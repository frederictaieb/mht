import os
import uuid
import cv2
import tempfile
import shutil
from fastapi import HTTPException

from app.core.paths import resolve_under
from app.utils.faces import pick_largest_face

class FaceSwapService:
    def __init__(self, runtime, img_dir: str, vid_dir: str, output_dir: str):
        self.runtime = runtime
        self.img_dir = img_dir
        self.vid_dir = vid_dir
        self.output_dir = output_dir

    def run(self, img_filename: str, vid_filename: str, output_filename: str | None = None):
        self.runtime.ensure_loaded()

        img_path = resolve_under(self.img_dir, img_filename)
        vid_path = resolve_under(self.vid_dir, vid_filename)

        if not os.path.exists(img_path):
            raise HTTPException(status_code=400, detail=f"Image introuvable: {img_path}")
        if not os.path.exists(vid_path):
            raise HTTPException(status_code=400, detail=f"Vidéo introuvable: {vid_path}")

        if output_filename:
            out_name = output_filename if output_filename.lower().endswith(".mp4") else output_filename + ".mp4"
        else:
            out_name = f"faceswap_{uuid.uuid4().hex}.mp4"

        out_path = os.path.join(self.output_dir, out_name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        img_src = cv2.imread(img_path)
        if img_src is None:
            raise HTTPException(status_code=400, detail="Impossible de lire l'image source.")

        faces_src = self.runtime.app_face.get(img_src)
        face_src = pick_largest_face(faces_src)
        if face_src is None:
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
                    frame = self.runtime.swapper.get(frame, tgt_face, face_src, paste_back=True)
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
