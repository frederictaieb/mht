# backend/app/api/routes/telepai_routes.py
import os
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from pydantic import BaseModel

from app.services.telepai_services import TelepaiServices
from app.services.database_services import DatabaseServices
from app.schemas.telepai import (
    CreateActressResponse,
    SayRequest,
    SayResponse,
    VoiceProfileCreateRequest, 
    MonologueCreateRequest,
    MonologueLineCreateRequest,
    GenerateMonologueLineAudioRequest
)

telepai_router = APIRouter(prefix="/telepai", tags=["telepai"])

#db_services = DatabaseServices(db_path="app/data/app.db", sql_dir="app/sql")
#telepai_services = TelepaiServices(db_services)

def get_db_services() -> DatabaseServices:
    return DatabaseServices(
        db_path="app/data/mht.db",
        sql_dir="app/db",
    )

def get_telepai_services() -> TelepaiServices:
    return TelepaiServices(db_service=get_db_services())

@telepai_router.post("/create_actress", response_model=CreateActressResponse)
async def create_actress(name: str = Form(...), file: UploadFile = File(...)):
    os.makedirs("app/data/telepai/input", exist_ok=True)
    safe_filename = f"{name}_{file.filename}"
    file_path = os.path.join("app/data/telepai/input", safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    actress = await get_telepai_services.create_actress(name=name, ref_audio_path=file_path)

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

### A COMPRENDRE ET A VERIFIER ###

@telepai_router.post("/voice-profile")
async def create_voice_profile(
    payload: VoiceProfileCreateRequest,
    service: TelepaiServices = Depends(get_telepai_services),
):
    return await service.create_voice_profile_from_avatar_name(
        avatar_name=payload.avatar_name,
        ref_audio_path=payload.ref_audio_path,
        note=payload.note,
    )

@telepai_router.post("/monologue")
async def create_monologue(
    payload: MonologueCreateRequest,
    service: TelepaiServices = Depends(get_telepai_services),
):
    return await service.create_monologue_for_scene_number(
        scene_number=payload.scene_number,
        title=payload.title,
    )

@telepai_router.post("/monologue-line")
async def create_monologue_line(
    payload: MonologueLineCreateRequest,
    service: TelepaiServices = Depends(get_telepai_services),
):
    return await service.create_monologue_line(
        monologue_id=payload.monologue_id,
        voice_profile_id=payload.voice_profile_id,
        line_order=payload.line_order,
        text=payload.text,
        generation_note=payload.generation_note,
    )

@telepai_router.post("/generate-monologue-line-audio")
async def generate_monologue_line_audio(
    payload: GenerateMonologueLineAudioRequest,
    service: TelepaiServices = Depends(get_telepai_services),
):
    return await service.generate_audio_for_monologue_line(
        monologue_line_id=payload.monologue_line_id,
        output_dir=payload.output_dir or "app/data/generated_audio",
    )