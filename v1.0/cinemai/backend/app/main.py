#backend/app/main.py
from fastapi import FastAPI
from app.api.routes.faceswap import router as faceswap_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/img", StaticFiles(directory=settings.IMG_DIR), name="img")
app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")

AVAILABLE_DIR = "/Users/fete/Desktop/code/mht/v1.0/cinemai/backend/app/data/input/vid/available"
IMAGE_DIR = "/Users/fete/Desktop/code/mht/v1.0/cinemai/backend/app/data/input/img"
OUTPUT_DIR = "/Users/fete/Desktop/code/mht/v1.0/cinemai/backend/app/data/output"


app.mount(
    "/faceswap/available/video",
    StaticFiles(directory=AVAILABLE_DIR),
    name="available_videos",
)

app.mount(
    "/faceswap/upload/image",
    StaticFiles(directory=IMAGE_DIR),
    name="uoload_images",
)

app.mount(
    "/faceswap/output/video",
    StaticFiles(directory=OUTPUT_DIR),
    name="output_videos",
)


app.include_router(faceswap_router)


