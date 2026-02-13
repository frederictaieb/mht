# main.py
# Face swap le plus simple possible (CPU) : 1 image source + 1 vidéo cible -> vidéo sortie
# ⚠️ À utiliser uniquement avec consentement des personnes concernées.

import argparse
import os
import subprocess
import tempfile

import cv2
from insightface.app import FaceAnalysis
import insightface


def pick_largest_face(faces):
    if not faces:
        return None

    def area(face):
        x1, y1, x2, y2 = face.bbox
        return float((x2 - x1) * (y2 - y1))

    return max(faces, key=area)


def ffmpeg_exists():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False


def extract_audio(in_video, out_audio):
    # Copie l’audio tel quel (si possible)
    return subprocess.run(
        ["ffmpeg", "-y", "-i", in_video, "-vn", "-acodec", "copy", out_audio],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def mux_audio(video_no_audio, audio_file, out_video):
    # Recolle l’audio (ré-encode en AAC pour compatibilité)
    return subprocess.run(
        ["ffmpeg", "-y", "-i", video_no_audio, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-shortest", out_video],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Image source (visage à copier)")
    ap.add_argument("--video", required=True, help="Vidéo cible")
    ap.add_argument("--out", default="out.mp4", help="Vidéo sortie")
    ap.add_argument("--swapper", default="./models/inswapper_128.onnx", help="Chemin vers inswapper_128.onnx")
    ap.add_argument("--keep-audio", action="store_true", help="Garder l'audio (nécessite ffmpeg)")
    args = ap.parse_args()

    if not os.path.isfile(args.swapper):
        raise FileNotFoundError(f"Modèle introuvable: {args.swapper}")

    # 1) Init InsightFace (CPU)
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=-1, det_size=(640, 640))

    # 2) Charger swapper ONNX
    swapper = insightface.model_zoo.get_model(args.swapper, providers=None)

    # 3) Charger image source + détecter visage
    src_img = cv2.imread(args.source)
    if src_img is None:
        raise ValueError(f"Impossible de lire l'image source: {args.source}")

    src_faces = app.get(src_img)
    src_face = pick_largest_face(src_faces)
    if src_face is None:
        raise RuntimeError("Aucun visage détecté dans l'image source.")

    # 4) Ouvrir vidéo
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la vidéo: {args.video}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 5) Ecrire vidéo temp sans audio
    tmp_dir = tempfile.mkdtemp(prefix="faceswap_")
    tmp_video = os.path.join(tmp_dir, "video_no_audio.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp_video, fourcc, fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError("Impossible d'initialiser le writer vidéo (mp4v).")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        # détecter visage cible (plus grand) et swap si trouvé
        tgt_faces = app.get(frame)
        tgt_face = pick_largest_face(tgt_faces)
        if tgt_face is not None:
            frame = swapper.get(frame, tgt_face, src_face, paste_back=True)

        writer.write(frame)

        if frame_idx % 60 == 0:
            print(f"{frame_idx} frames...")

    cap.release()
    writer.release()

    # 6) Option audio
    if args.keep_audio and ffmpeg_exists():
        tmp_audio = os.path.join(tmp_dir, "audio.aac")
        if extract_audio(args.video, tmp_audio) and mux_audio(tmp_video, tmp_audio, args.out):
            print(f"OK (avec audio) -> {args.out}")
            return

        # fallback : sans audio
        print("Audio: échec -> sortie sans audio.")

    os.replace(tmp_video, args.out)
    print(f"OK -> {args.out}")


if __name__ == "__main__":
    main()
