# backend/app/schemas/telepai.py
from pydantic import BaseModel, Field


class CreateActressResponse(BaseModel):
    name: str
    ref_audio: str
    ref_text: str


class SayRequest(BaseModel):
    text: str
    instruct: str

class SayResponse(BaseModel):
    actress_name: str
    output_file: str