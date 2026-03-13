# backend/app/schemas/telepai/speech.py
from pydantic import BaseModel, ConfigDict


class SpeechCreate(BaseModel):
    presence_id: int
    title: str | None = None


class SpeechResponse(BaseModel):
    id: int
    presence_id: int
    title: str | None = None

    model_config = ConfigDict(from_attributes=True)