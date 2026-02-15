# backend/app/services/faceswap_service.py
import os
import uuid
import cv2
import tempfile
import shutil
import logging
import time
import subprocess
from shutil import which

from fastapi import HTTPException

from app.core.paths import resolve_under
from app.utils.faces import pick_largest_face

log = logging.getLogger("uvicorn.error")


class FaceSwapService:
    def __init__(self, runtime, img_dir: str, vid_dir: str, output_dir: str):
        self.runtime = runtime
        self.img_dir = img_dir
        self.vid_dir = vid_dir
        self.output_dir = output_dir

    def _ensure_ffmpeg(self) -> None:
        if which("ffmpeg") is None:
            raise HTTPException(
                status_code=500,
                detail="ffmpeg introuvable. Installe ffmpeg (brew install ffmpeg / apt install ffmpeg).",
            )

    def _encode_h264_mp4(self, in_path: str, out_path: str) -> None:
        """
        Encode web-friendly MP4:
        - H.264 (libx264)
        - yuv420p (compatibilité navigateurs)
        - faststart (moov atom au début -> seek/preview)
        - pas d'audio (comme ton flux OpenCV)
        """
        self._ensure_ffmpeg()

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            in_path,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "high",
            "-level",
            "4.0",
            "-movflags",
            "+faststart",
            "-an",
            out_path,
        ]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            err = p.stderr.decode("utf-8", "ignore")
            log.error("ffmpeg failed: %s", err)
            raise HTTPException(status_code=500, detail="FFmpeg a échoué lors de l'encodage H.264.")

    def run(self, img_filename: str, vid_filename: str):
        rid = int(time.time() * 1000)
        log.info("faceswap start img=%s vid=%s", img_filename, vid_filename)
        self.runtime.ensure_loaded()

        img_path = resolve_under(self.img_dir, img_filename)
        vid_path = resolve_under(self.vid_dir, vid_filename)

        if not os.path.exists(img_path):
            raise HTTPException(status_code=400, detail=f"Image not found: {img_path}")
        if not os.path.exists(vid_path):
            raise HTTPException(status_code=400, detail=f"Video not found: {vid_path}")

        # Nom de sortie (comme ton code)
        base_vid = os.path.basename(vid_filename).rsplit("-", 1)[-1]
        out_name = f"fs-{base_vid}"
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

        # 1) OpenCV écrit un fichier "raw" simple et stable (AVI/MJPG)
        tmp_raw = os.path.join(tmp_dir, "video_raw.avi")

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(tmp_raw, fourcc, fps, (w, h))
        if not writer.isOpened():
            cap.release()
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise HTTPException(status_code=500, detail="Impossible d'initialiser le writer vidéo (MJPG).")

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

        # 2) FFmpeg encode final en MP4 H.264 web-compatible (+faststart)
        tmp_mp4 = os.path.join(tmp_dir, "video_h264.mp4")
        self._encode_h264_mp4(tmp_raw, tmp_mp4)

        # Remplace le fichier final
        os.replace(tmp_mp4, out_path)

        # Clean
        shutil.rmtree(tmp_dir, ignore_errors=True)

        log.info("faceswap end frames=%s swapped=%s", frame_idx, swapped_frames)

        st = os.stat(out_path)
        log.info("output stats: path=%s size=%s mtime=%s", out_path, st.st_size, st.st_mtime)

        return {
            "output_file": out_name,
            "output_path": out_path,
            "frames": frame_idx,
            "swapped_frames": swapped_frames,
        }
