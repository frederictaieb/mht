import os
import uuid
import cv2
import tempfile
import shutil
from fastapi import HTTPException

from app.core.paths import resolve_under
from app.utils.faces import pick_largest_face

class FaceSwapService:
    def __init__(self, runtime, input_dir: str, output_dir: str):
        self.runtime = runtime
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self, source_image_path: str, target_video_path: str, output_name: str | None = None):
        self.runtime.ensure_loaded()

        src_path = resolve_under(self.input_dir, source_image_path)
        vid_path = resolve_under(self.input_dir, target_video_path)

        if not os.path.exists(src_path):
            raise HTTPException(status_code=400, detail=f"Image introuvable: {source_image_path}")
        if not os.path.exists(vid_path):
            raise HTTPException(status_code=400, detail=f"Vidéo introuvable: {target_video_path}")

        if output_name:
            out_name = output_name if output_name.lower().endswith(".mp4") else output_name + ".mp4"
        else:
            out_name = f"faceswap_{uuid.uuid4().hex}.mp4"

        out_path = os.path.join(self.output_dir, out_name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        src_img = cv2.imread(src_path)
        if src_img is None:
            raise HTTPException(status_code=400, detail="Impossible de lire l'image source.")

        src_faces = self.runtime.app_face.get(src_img)
        src_face = pick_largest_face(src_faces)
        if src_face is None:
            raise HTTPException(status_code=400, detail="Aucun visage détecté dans l'image source.")

        cap = cv2.VideoCapture(vid_path)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Impossible d'ouvrir la vidéo.")

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        tmp_dir = tempfile.mkdtemp(prefix="faceswap_")
        tmp_out = os.path.join(tmp_dir, "video_no_audio.mp4")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(tmp_out, fourcc, fps, (w, h))
        if not writer.isOpened():
            cap.release()
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise HTTPException(status_code=500, detail="Impossible d'initialiser le writer vidéo (mp4v).")

        frame_idx = 0
        swapped_frames = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                tgt_faces = self.runtime.app_face.get(frame)
                tgt_face = pick_largest_face(tgt_faces)

                if tgt_face is not None:
                    frame = self.runtime.swapper.get(frame, tgt_face, src_face, paste_back=True)
                    swapped_frames += 1

                writer.write(frame)
                frame_idx += 1
        finally:
            cap.release()
            writer.release()

        os.replace(tmp_out, out_path)
        shutil.rmtree(tmp_dir, ignore_errors=True)

        return {
            "output_file": out_name,
            "output_path": out_path,
            "frames": frame_idx,
            "swapped_frames": swapped_frames,
        }
