# backend/app/api/routes/faceswap.py
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

from fastapi.responses import FileResponse
from app.services.job_store import JobStore
from app.services.video_pool import VideoPool

from app.utils.folder import _purge_dir, _copy_tree_contents

from fastapi.responses import FileResponse

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
output_service = DirectoryService(settings.OUTPUT_DIR, "vid")

available_service = DirectoryService(os.path.join(settings.VID_DIR, "available"), "vid")

store = JobStore(settings.JOBS_FILE)
pool = VideoPool(settings.VID_DIR)  # utilise VID_DIR/available|in_progress|used

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

@router.delete("/vid/delete")
def vid_delete():
    return video_service.dir_delete()

@router.post("/vid/upload")
def vid_upload(f: UploadFile = File(...)):
    return video_service.dir_upload(f)



@router.post("/submit")
async def submit_faceswap(f: UploadFile = File(...)):
    # Check file extension
    ext = os.path.splitext(f.filename or "")[1].lower()
    if ext not in (".jpg", ".jpeg", ".png"):
        raise HTTPException(status_code=415, detail="Only jpg/jpeg/png allowed")

    # Create a new job id
    job_id = uuid.uuid4().hex

    # Save the image with a new unique filename
    img_name = f"{job_id}{ext}"
    img_path = os.path.join(settings.IMG_DIR, img_name)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    try:
        with open(img_path, "wb") as out:
            shutil.copyfileobj(f.file, out)
    finally:
        f.file.close()

    # Reserve the next available video
    reserved = pool.reserve_next(job_id)

    # no video available
    if not reserved:
        store.create(job_id, img_name)
        store.update(job_id, status="waiting_for_video", error="No more videos available")
        return {"job_id": job_id, "status": "waiting_for_video"}

    # vid relative sous VID_DIR (important pour resolve_under)
    vid_rel = f"in_progress/{reserved}"

    # Create new job 
    store.create(job_id, img_name)
    store.update(job_id, status="running", reserved_video=vid_rel)

    # Runing faceswap 
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(
            faceswap_executor,
            faceswap_service.run,
            img_name,
            vid_rel
        )
    except Exception as e:
        # échec : on remet la vidéo dans available
        pool.release_back(reserved)
        store.update(job_id, status="failed", error=str(e))
        raise

    # The video is move in used folder
    pool.mark_used(reserved)

    # Store is updated
    store.update(
        job_id,
        status="done",
        output_file=result["output_file"],
        frames=result["frames"],
        swapped_frames=result["swapped_frames"],
        error=None
    )

    return {"job_id": job_id, "status": "done", "output_file": result["output_file"]}


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


#@router.get("/output/{filename}")
#def get_output(filename: str):
#    path = os.path.join(settings.OUTPUT_DIR, filename)
#    if not os.path.exists(path):
#        raise HTTPException(status_code=404, detail="File not found")
#    return FileResponse(path, media_type="video/mp4", filename=filename)

@router.post("/reset")
def faceswap_reset():
    """
    Supprime:
      - vid/available, vid/used, vid/in_progress
      - img
      - output
    Puis copie vid/archive -> vid/available
    """

    available_dir = os.path.join(settings.VID_DIR, "available")
    used_dir = os.path.join(settings.VID_DIR, "used")
    in_progress_dir = os.path.join(settings.VID_DIR, "in_progress")
    archive_dir = os.path.join(settings.VID_DIR, "archive")

    # 1) purge
    deleted = {
        "available": _purge_dir(available_dir),
        "used": _purge_dir(used_dir),
        "in_progress": _purge_dir(in_progress_dir),
        "img": _purge_dir(settings.IMG_DIR),
        "output": _purge_dir(settings.OUTPUT_DIR),
    }

    # 2) restore archive -> available
    copied = _copy_tree_contents(archive_dir, available_dir)

    return {
        "type": "reset",
        "deleted": deleted,
        "restored_from_archive": {
            "archive_dir": archive_dir,
            "available_dir": available_dir,
            "files_copied": copied,
        }
    }

@router.get("/available/list")
def available_list():
    available_dir = os.path.join(settings.VID_DIR, "available")
    files = sorted([
        f 
        for f in os.listdir(available_dir)
        if os.path.isfile(os.path.join(available_dir, f)) and not f.startswith(".")
    ])

    return {
        "files": files
    }


@router.get("/output/list")
def output_list():
    return output_service.dir_list()

@router.get("/output/{filename}")
def get_output(filename: str):
    path = os.path.join(settings.OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="video/mp4", filename=filename)
