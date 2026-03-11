# backend/app/schemas/telepai.py
from pydantic import BaseModel, Field

class SayRequest(BaseModel):
    text: str

class CreateActressResponse(BaseModel):
    name: str
    ref_audio: str
    ref_text: str

class SayResponse(BaseModel):
    actress_name: str
    file_path: str
    audio_url: str