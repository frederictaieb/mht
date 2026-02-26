#backend/app/main.py
from fastapi import FastAPI
from app.api.cinemai import router as cinemai_router
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

app.mount(
    "/cinemai/static/available_videos",
    StaticFiles(directory=settings.AVAILABLE_DIR),
    name="available_videos",
)

app.mount(
    "/cinemai/static/upload_image",
    StaticFiles(directory=settings.IMG_DIR),
    name="uoload_images",
)

app.mount(
    "/cinemai/static/output_video",
    StaticFiles(directory=settings.OUTPUT_DIR),
    name="output_videos",
)


app.include_router(cinemai_router)


