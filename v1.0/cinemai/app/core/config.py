import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # app/..
    INPUT_DIR: str = os.path.join(BASE_DIR, "data/input")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "data/output")

    MODELS_DIR: str = os.path.join(BASE_DIR, "data/ai_models")
    SWAPPER_MODEL: str = os.path.join(MODELS_DIR, "inswapper_128.onnx")

    # InsightFace
    DET_SIZE: tuple = (640, 640)
    CTX_ID: int = -1  # -1 CPU, 0 GPU

settings = Settings()
