# backend/app/core/config.py
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # app/..

    IMG_DIR: str = os.path.join(BASE_DIR, "data/input/img")
    VID_DIR: str = os.path.join(BASE_DIR, "data/input/vid")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "data/output")

    JOBS_FILE: str = os.path.join(BASE_DIR, "data/jobs.json")

    MODELS_DIR: str = os.path.join(BASE_DIR, "data/ai_models")
    SWAPPER_MODEL: str = os.path.join(MODELS_DIR, "inswapper_128.onnx")

    # InsightFace
    DET_SIZE: tuple = (640, 640)
    CTX_ID: int = -1  # -1 CPU, 0 GPU

settings = Settings()
