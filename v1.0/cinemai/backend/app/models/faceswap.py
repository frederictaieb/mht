# backend/app/models/faceswap.py
from pydantic import BaseModel

class FaceSwapSingleRequest(BaseModel):
    img: str
    vid: str