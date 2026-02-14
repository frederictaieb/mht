import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.services.insightface_runtime import InsightFaceRuntime
from app.services.faceswap_service import FaceSwapService

router = APIRouter(prefix="/faceswap", tags=["faceswap"])

runtime = InsightFaceRuntime(
    model_path=settings.SWAPPER_MODEL,
    ctx_id=settings.CTX_ID,
    det_size=settings.DET_SIZE,
    providers=["CPUExecutionProvider"],
)

service = FaceSwapService(runtime, settings.INPUT_DIR, settings.OUTPUT_DIR)

class FaceSwapPathsRequest(BaseModel):
    source_image_path: str
    target_video_path: str
    output_name: str | None = None

@router.post("/single")
def faceswap_single(payload: FaceSwapPathsRequest):
    return service.run(
        source_image_path=payload.source_image_path,
        target_video_path=payload.target_video_path,
        output_name=payload.output_name,
    )

@router.post("/upload")
def upload_image():
    return


@router.delete("/delete")
def delete_images():
    deleted = 0
    INPUT_DIR = settings.INPUT_DIR

    if not os.path.exists(INPUT_DIR):
        raise HTTPException(status_code=404, detail="Input directory not found")
    
    if not os.path.isdir(INPUT_DIR):
        raise HTTPException(status_code=400, detail="INPUT_DIR n'est pas un dossier")

    for filename in os.listdir(INPUT_DIR):
        path = os.path.join(INPUT_DIR, filename)

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

