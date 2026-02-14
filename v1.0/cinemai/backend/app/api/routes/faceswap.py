import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService
from app.services.filemanagement_service import ImageService
from app.models.faceswap import FaceSwapSingleRequest

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

@router.post("/single")
def faceswap_single(payload: FaceSwapSingleRequest):
    return faceswap_service.run(payload.img, payload.vid)

@router.post("/img/list")
def img_list():
    return image_service.img_list()

@router.delete("/img/delete")
def img_delete():
    return image_service.img_delete()

@router.post("/img/upload")
def img_upload(f: UploadFile = File(...)):
    return image_service.img_upload(f)