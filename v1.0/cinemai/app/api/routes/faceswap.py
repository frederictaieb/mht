from fastapi import APIRouter
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
