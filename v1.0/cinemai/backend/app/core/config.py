# backend/app/core/config.py
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self):
        # --- Config (.env) ---
        self.CINEMAI_REQUIRED_VIDEOS = int(os.getenv("CINEMAI_REQUIRED_VIDEOS", 10))

        # --- Paths ---
        base_dir = Path(__file__).resolve().parents[1]

        self.BASE_DIR = base_dir

        self.IMG_DIR = base_dir / "data/cinemai/input/img"
        self.ARCHIVE_DIR = base_dir / "data/cinemai/input/vid/archive"
        self.AVAILABLE_DIR = base_dir / "data/cinemai/input/vid/available"

        self.OUTPUT_DIR = base_dir / "data/cinemai/output"

        self.MODELS_DIR = base_dir / "data/ai_models"
        self.SWAPPER_MODEL = self.MODELS_DIR / "inswapper_128.onnx"

        # --- InsightFace ---
        self.DET_SIZE = (640, 640)
        self.CTX_ID = -1

    @property
    def PROD_DIR(self) -> Path:
        today_str = datetime.now().strftime("%Y%m%d")
        path = self.BASE_DIR / "data/cinemai/prod" / today_str
        path.mkdir(parents=True, exist_ok=True)
        return path

# ✅ instance globale (comme avant)
settings = Settings()