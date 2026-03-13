# backend/app/schemas/telepai/avatar.py
from pydantic import BaseModel, ConfigDict

class AvatarCreate(BaseModel):
    name: str
    actress_id: int

class AvatarResponse(BaseModel):
    id: int
    name: str
    actress_id: int

    model_config = ConfigDict(from_attributes=True)
