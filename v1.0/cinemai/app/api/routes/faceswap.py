import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService

import uuid
import shutil

router = APIRouter(prefix="/faceswap", tags=["faceswap"])

runtime = InsightFaceRuntime(
    model_path=settings.SWAPPER_MODEL,
    ctx_id=settings.CTX_ID,
    det_size=settings.DET_SIZE,
    providers=["CPUExecutionProvider"],
)

service = FaceSwapService(runtime, settings.IMG_DIR, settings.VID_DIR, settings.OUTPUT_DIR)

class FaceSwapPathsRequest(BaseModel):
    img: str
    vid: str
    output: str | None = None

@router.post("/single")
def faceswap_single(payload: FaceSwapPathsRequest):
    return service.run(
        img_filename=payload.img,
        vid_filename=payload.vid,
        output_filename=payload.output,
    )


ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}

@router.post("/img/list")
def img_list():
    img_dir = settings.IMG_DIR

    if not os.path.exists(img_dir):
        raise HTTPException(status_code=404, detail="Dossier img introuvable")

    if not os.path.isdir(img_dir):
        raise HTTPException(status_code=400, detail="Le chemin n'est pas un dossier")

    files = [
        f for f in os.listdir(img_dir)
        if os.path.isfile(os.path.join(img_dir, f))
    ]

    return {
        "directory": "input/img",
        "count": len(files),
        "files": files
    }

    return

@router.post("/img/upload")
def img_upload(file: UploadFile = File(...)):
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


    return


@router.delete("/img/delete")
def img_delete():
    deleted = 0
    IMG_DIR = settings.IMG_DIR

    if not os.path.exists(IMG_DIR):
        raise HTTPException(status_code=404, detail="Img directory not found")
    
    if not os.path.isdir(IMG_DIR):
        raise HTTPException(status_code=400, detail="IMG_DIR n'est pas un dossier")

    for filename in os.listdir(IMG_DIR):
        path = os.path.join(IMG_DIR, filename)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
                deleted += 1
            elif os.path.isdir(path):
                shutil.rmtree(path)
                deleted += 1
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")

    return {
        "message": "input directory cleared",
        "deleted_items": deleted
    }
    return

