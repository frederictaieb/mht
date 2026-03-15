# backend/app/schemas/telepai/line.py
from pydantic import BaseModel, ConfigDict


class LineCreate(BaseModel):
    speech_id: int
    profile_id: int
    line_order: int
    content: str


class LineResponse(BaseModel):
    id: int
    speech_id: int
    profile_id: int
    line_order: int
    content: str

    model_config = ConfigDict(from_attributes=True)