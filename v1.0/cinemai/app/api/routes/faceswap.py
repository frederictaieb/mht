import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService
from app.services.filemanagement_service import ImageService

import uuid
import shutil

router = APIRouter(prefix="/faceswap", tags=["faceswap"])

runtime = InsightFaceRuntime(
    model_path=settings.SWAPPER_MODEL,
    ctx_id=settings.CTX_ID,
    det_size=settings.DET_SIZE,
    providers=["CPUExecutionProvider"],
)

faceswap_service = FaceSwapService(runtime, settings.IMG_DIR, settings.VID_DIR, settings.OUTPUT_DIR)
image_service = ImageService(settings.IMG_DIR)

class FaceSwapPathsRequest(BaseModel):
    img: str
    vid: str
    output: str | None = None

@router.post("/single")
def faceswap_single(payload: FaceSwapPathsRequest):
    return faceswap_service.run(
        img_filename=payload.img,
        vid_filename=payload.vid,
        output_filename=payload.output,
    )

@router.post("/img/list")
def img_list():
    return image_service.img_list()

@router.delete("/img/delete")
def img_delete():
    return image_service.img_delete()

@router.post("/img/upload")
def img_upload(file: UploadFile = File(...)):
    ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}
    UPLOAD_DIR = settings.IMG_DIR

    # 1) Vérif mime type
    if file.content_type not in ALLOWED_IMAGE_MIME:
        raise HTTPException(
            status_code=400,
            detail=f"Type interdit: {file.content_type}. Autorisés: {sorted(ALLOWED_IMAGE_MIME)}"
        )
    
    # 2) Extension (fallback si filename vide)
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        # on force une extension cohérente au mime
        ext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }[file.content_type]

    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, safe_name)

    # 4) Écriture sur disque
    try:
        with open(dest_path, "wb") as out:
            shutil.copyfileobj(file.file, out)
    finally:
        file.file.close()

    return {
        "message": "uploaded",
        "filename": safe_name,
        "path": dest_path,  # tu peux enlever ça si tu préfères ne pas exposer le path interne
    }


