import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService
from app.services.filemanagement_service import DirectoryService
from app.models.faceswap import FaceSwapSingleRequest

import uuid
import shutil

import threading

# app/api/routes/faceswap.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

faceswap_executor = ThreadPoolExecutor(max_workers=1)

router = APIRouter(prefix="/faceswap", tags=["faceswap"])

runtime = InsightFaceRuntime(
    model_path=settings.SWAPPER_MODEL,
    ctx_id=settings.CTX_ID,
    det_size=settings.DET_SIZE,
    providers=["CPUExecutionProvider"],
)

faceswap_service = FaceSwapService(runtime, settings.IMG_DIR, settings.VID_DIR, settings.OUTPUT_DIR)
image_service = DirectoryService(settings.IMG_DIR, "img")
video_service = DirectoryService(settings.VID_DIR, "vid")

faceswap_executor = ThreadPoolExecutor(max_workers=1)

@router.post("/single")
async def faceswap_single(payload: FaceSwapSingleRequest):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        faceswap_executor,
        faceswap_service.run,
        payload.img,
        payload.vid
    )

@router.post("/img/list")
def img_list():
    return image_service.dir_list()

@router.delete("/img/delete")
def img_delete():
    return image_service.dir_delete()

@router.post("/img/upload")
def img_upload(f: UploadFile = File(...)):
    return image_service.dir_upload(f)

@router.post("/vid/list")
def vid_list():
    return video_service.dir_list()

@router.post("/vid/delete")
def vid_delete():
    return video_service.dir_delete()

@router.post("/vid/upload")
def vid_upload(f: UploadFile = File(...)):
    return image_service.vid_upload(f)