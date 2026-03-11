from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.services.telepai_services import TelepaiServices
from typing import Optional
from pydantic import BaseModel

telepai_router = APIRouter(prefix="/telepai", tags=["telepai"])

telepai_service = TelepaiServices()


@telepai_router.post("/voice_clone")
async def create_voice_clone(
    actress_name: str = Form(...),
    character_name: str = Form(...),
    style_name: str = Form(...),
    file: UploadFile = File(...),
):
    file_path = telepai_service.create_voice_clone(
        actress_name=actress_name,
        character_name=character_name,
        style_name=style_name,
        upload_file=file,
    )

    return {
        "message": "Voice clone créé avec succès.",
        "file_path": file_path,
    }


@telepai_router.get("/voice_clone")
async def get_voice_clone(
    actress_name: str,
    character_name: str,
    style_name: str,
):
    file_path = telepai_service.get_voice_clone(
        actress_name=actress_name,
        character_name=character_name,
        style_name=style_name,
    )

    if not file_path:
        raise HTTPException(status_code=404, detail="Voice clone introuvable.")

    return {
        "file_path": file_path,
    }


@telepai_router.delete("/voice_clone")
async def delete_voice_clone(
    actress_name: str,
    character_name: str,
    style_name: str,
):
    deleted = telepai_service.delete_voice_clone(
        actress_name=actress_name,
        character_name=character_name,
        style_name=style_name,
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Voice clone introuvable.")

    return {
        "message": "Voice clone supprimé avec succès.",
    }


@telepai_router.get("/voice_clones")
async def list_voice_clones():
    files = telepai_service.list_voice_clones()
    return {
        "items": files,
        "count": len(files),
    }


@telepai_router.get("/voice_clone/stt")
async def stt_voice_clone(
    actress_name: str,
    character_name: str,
    style_name: str,
):
    file_path = telepai_service.get_voice_clone(
        actress_name=actress_name,
        character_name=character_name,
        style_name=style_name,
    )

    if not file_path:
        raise HTTPException(status_code=404, detail="Voice clone introuvable.")

    result = await telepai_service.stt(file_path)

    return {
        "file_path": file_path,
        **result,
    }

class TTSCloneSegment(BaseModel):
    text: str
    instruct: Optional[str] = None


class TTSCloneRequest(BaseModel):
    actress_name: str
    character_name: str
    style_name: str
    ref_text: str
    segments: list[TTSCloneSegment]
    language: str = "French"
    silence_sec: float = 0.18
    output_filename: Optional[str] = None

@telepai_router.post("/voice-clone/generate")
async def generate_voice_clone_audio(payload: TTSCloneRequest):
    result = await telepai_service.generate_voice_clone_audio(
        actress_name=payload.actress_name,
        character_name=payload.character_name,
        style_name=payload.style_name,
        ref_text=payload.ref_text,
        segments=[segment.model_dump() for segment in payload.segments],
        language=payload.language,
        silence_sec=payload.silence_sec,
        output_filename=payload.output_filename,
    )
    return result