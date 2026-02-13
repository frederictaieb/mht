from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import cv2
import tempfile
import shutil
import insightface
from insightface.app import FaceAnalysis
    
def pick_largest_face(faces):
    if not faces:
        return None

    def area(face):
        x1, y1, x2, y2 = face.bbox
        return float((x2 - x1) * (y2 - y1))

    return max(faces, key=area)

def ensure_parent_dir(path: str):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)

app = FastAPI()

@app.post("/faceswap_single")
async def faceswap_single(
    source_image: UploadFile = File(...),
    target_video: UploadFile = File(...)
):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    swapper_model_path = os.path.join(BASE_DIR, "models", "inswapper_128.onnx")

    if not os.path.exists(swapper_model_path):
        raise HTTPException(status_code=500, detail="Modèle swapper introuvable.")

    # --- Workspace temporaire ---
    tmp_dir = tempfile.mkdtemp(prefix="faceswap_")
    source_image_path = os.path.join(tmp_dir, "source.jpg")
    input_video_path  = os.path.join(tmp_dir, "input.mp4")
    output_video_path = os.path.join(tmp_dir, "output.mp4")
    tmp_video_no_audio = os.path.join(tmp_dir, "video_no_audio.mp4")

    # --- Sauvegarde fichiers uploadés ---
    with open(source_image_path, "wb") as f:
        shutil.copyfileobj(source_image.file, f)

    with open(input_video_path, "wb") as f:
        shutil.copyfileobj(target_video.file, f)

    # --- Init InsightFace ---
    app_face = FaceAnalysis(name="buffalo_l")
    app_face.prepare(ctx_id=-1, det_size=(640, 640))

    swapper = insightface.model_zoo.get_model(
        swapper_model_path,
        providers=["CPUExecutionProvider"],
    )

    # --- Load image source ---
    src_img = cv2.imread(source_image_path)
    if src_img is None:
        raise HTTPException(status_code=400, detail="Impossible de lire l'image source.")

    src_faces = app_face.get(src_img)
    src_face = pick_largest_face(src_faces)
    if src_face is None:
        raise HTTPException(status_code=400, detail="Aucun visage détecté dans l'image source.")

    # --- Open video ---
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Impossible d'ouvrir la vidéo.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp_video_no_audio, fourcc, fps, (w, h))

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        tgt_faces = app_face.get(frame)
        tgt_face = pick_largest_face(tgt_faces)

        if tgt_face is not None:
            frame = swapper.get(frame, tgt_face, src_face, paste_back=True)

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    # Pour l'instant sans audio (comme ton fallback)
    os.replace(tmp_video_no_audio, output_video_path)

    return FileResponse(
        output_video_path,
        media_type="video/mp4",
        filename="faceswapped.mp4"
    )