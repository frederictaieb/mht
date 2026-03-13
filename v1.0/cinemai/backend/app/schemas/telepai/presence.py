# backend/app/schemas/telepai/presence.py
from pydantic import BaseModel, ConfigDict


class PresenceCreate(BaseModel):
    chapter_id: int
    avatar_id: int

class PresenceResponse(BaseModel):
    id: int
    chapter_id: int
    avatar_id: int

    model_config = ConfigDict(from_attributes=True)