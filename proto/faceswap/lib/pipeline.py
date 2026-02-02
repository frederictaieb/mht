import os
import shutil
import tempfile

import cv2

from .utils import pick_largest_face, ensure_dir
from .media import ffmpeg_exists, extract_audio, mux_audio


def process_one(
    *,
    app,
    swapper,
    source_img_path: str,
    video_in_path: str,
    out_path: str,
    max_width: int,
    every: int,
    keep_audio: bool,
    logger,
):
    """
    Traite une vidéo: détecte visage source, boucle frames, swap, écrit tmp, remux audio.
    """
    if not os.path.isfile(source_img_path):
        raise FileNotFoundError(source_img_path)
    if not os.path.isfile(video_in_path):
        raise FileNotFoundError(video_in_path)

    src_img = cv2.imread(source_img_path)
    if src_img is None:
        raise ValueError(f"Impossible de lire l'image source: {source_img_path}")

    src_face = pick_largest_face(app.get(src_img))
    if src_face is None:
        raise RuntimeError("Aucun visage détecté dans l'image source")

    cap = cv2.VideoCapture(video_in_path)
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la vidéo: {video_in_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 25.0
        logger.warning("FPS non détecté -> fallback 25.0")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    scale = 1.0
    if max_width and w > max_width:
        scale = max_width / w
        w = int(w * scale)
        h = int(h * scale)

    tmp_dir = tempfile.mkdtemp(prefix="faceswap_")
    try:
        tmp_video = os.path.join(tmp_dir, "video_no_audio.mp4")

        writer = cv2.VideoWriter(
            tmp_video,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h)
        )
        if not writer.isOpened():
            raise RuntimeError("VideoWriter n'a pas pu être ouvert (codec/fps/size).")

        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            i += 1

            if scale != 1.0:
                frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)

            if every > 1 and (i % every != 0):
                writer.write(frame)
                continue

            tgt_face = pick_largest_face(app.get(frame))
            if tgt_face is not None:
                frame = swapper.get(frame, tgt_face, src_face, paste_back=True)

            writer.write(frame)

        cap.release()
        writer.release()

        ensure_dir(os.path.dirname(out_path) or ".")

        if keep_audio and ffmpeg_exists():
            tmp_audio = os.path.join(tmp_dir, "audio.aac")

            code, _, err = extract_audio(video_in_path, tmp_audio)
            if code != 0:
                logger.warning(f"Extraction audio échouée, sortie sans audio. err={err}")
                os.replace(tmp_video, out_path)
                return

            code, _, err = mux_audio(tmp_video, tmp_audio, out_path)
            if code != 0:
                logger.warning(f"Mux audio échoué, sortie sans audio. err={err}")
                os.replace(tmp_video, out_path)
                return

            logger.info(f"OK (avec audio) -> {out_path}")
        else:
            os.replace(tmp_video, out_path)
            logger.info(f"OK -> {out_path}")

    finally:
        try:
            cap.release()
        except Exception:
            pass
        shutil.rmtree(tmp_dir, ignore_errors=True)
