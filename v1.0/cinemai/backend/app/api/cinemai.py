# backend/app/api/routes/faceswap.py
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService
from app.models.faceswap import FaceSwapSingleRequest

import uuid
import shutil

import threading

from fastapi.responses import FileResponse

from app.utils.folder import _purge_dir, _copy_tree_contents

from fastapi.responses import FileResponse

# app/api/cinemai.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

faceswap_executor = ThreadPoolExecutor(max_workers=1)

router = APIRouter(prefix="/cinemai", tags=["cinemai"])

runtime = InsightFaceRuntime(
    model_path=settings.SWAPPER_MODEL,
    ctx_id=settings.CTX_ID,
    det_size=settings.DET_SIZE,
    providers=["CPUExecutionProvider"],
)

faceswap_service = FaceSwapService(runtime, settings.IMG_DIR, settings.AVAILABLE_DIR, settings.OUTPUT_DIR)

faceswap_executor = ThreadPoolExecutor(max_workers=1)

# List all the available videos
@router.get("/available_videos")
def available_videos():
    available_dir = settings.AVAILABLE_DIR
    files = sorted([
        f 
        for f in os.listdir(available_dir)
        if os.path.isfile(os.path.join(available_dir, f)) and not f.startswith(".")
    ])

    return {
        "files": files
    }

# Upload Image
@router.post("/upload_image")
async def upload_image(
    image: UploadFile = File(...),
    name: str = Form(...),
):
    ext = ".jpg" if image.content_type == "image/jpeg" else ".png"

    img_dir = Path(settings.IMG_DIR)
    img_name =f"{Path(name).stem}{ext}"
    path = img_dir / img_name

    with path.open("wb") as f:
        f.write(await image.read())

    return {"ok": True, "img_name": img_name}

# Create Faceswap from available video et uploaded photo
@router.post("/generate_faceswap")
async def generate_faceswap(
    video_name: str = Form(...),
    image_name: str = Form(...),
):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        faceswap_executor,
        lambda: faceswap_service.run(image_name, video_name)
    )

#
#@router.get("/output/list")
#def output_list():
#    return output_service.dir_list()

@router.get("/output/{filename}")
def get_output(filename: str):
    path = os.path.join(settings.OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="video/mp4", filename=filename)

def clear_directory(folder_path: str, delete_dirs: bool = False):
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

            elif os.path.isdir(file_path) and delete_dirs:
                shutil.rmtree(file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset")
async def reset():
    clear_directory("/path/folder1")
    clear_directory("/path/folder2")
    clear_directory("/path/folder3")

    return {"message": "Tous les dossiers ont été nettoyés"}