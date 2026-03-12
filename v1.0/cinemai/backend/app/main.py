#backend/app/main.py

from app.utils.logger import setup_logging, get_logger
setup_logging()

from fastapi import FastAPI

from app.api.cinemai import cinemai_router
from app.api.telepai import telepai_router


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings 

from app.services.database_services import DatabaseServices

logger = get_logger(__name__)
logger.info("Starting FastAPI...")
app = FastAPI()

@app.on_event("startup")
def startup_event():
    db_service = DatabaseServices(
        db_path="app/data/mht.db",
        sql_dir="app/db",
    )
    db_service.create_tables()

    if db_service.is_actress_table_empty():
        db_service.fill_tables()

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
app.include_router(telepai_router)




