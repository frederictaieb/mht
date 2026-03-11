# backend/app/api/routes/telepai.py
import os
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.telepai_services import TelepaiServices

from app.schemas.telepai import (
    CreateActressResponse,
    SayRequest,
    SayResponse,
)

telepai_router = APIRouter(prefix="/telepai", tags=["telepai"])
telepai_service = TelepaiServices()

@telepai_router.post("/create_actress", response_model=CreateActressResponse)
async def create_actress(name: str = Form(...), file: UploadFile = File(...)):
    os.makedirs("app/data/telepai/input", exist_ok=True)
    safe_filename = f"{name}_{file.filename}"
    file_path = os.path.join("app/data/telepai/input", safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    actress = await telepai_service.create_actress(name=name, ref_audio_path=file_path)

    return CreateActressResponse(
        name=actress.name,
        ref_audio=actress.default_ref_audio,
        ref_text=actress.default_ref_text,
    )


@telepai_router.post("/{name}/say", response_model=SayResponse)
async def actress_say(name: str, text: str = Form(...)):
    actress = telepai_service.get_actress(name)
    file_path = await actress.say(text)

    return SayResponse(
        actress_name=name,
        file_path=file_path,
        audio_url=f"/telepai/{name}/get"
    )


@telepai_router.get("/{name}/get")
async def get_actress_audio(name: str):
    actress = telepai_service.get_actress(name)
    output_path = os.path.join("app/data/telepai/output", f"{actress.name}_voice_clone.wav")

    if not os.path.exists(output_path):
        raise HTTPException(
            status_code=404,
            detail="Aucun fichier audio généré pour cette actrice."
        )

    return FileResponse(
        path=output_path,
        media_type="audio/wav",
        filename=f"{actress.name}_voice_clone.wav",
    )