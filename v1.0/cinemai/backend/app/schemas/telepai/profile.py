# backend/app/schemas/telepai/profile.py
from pydantic import BaseModel, ConfigDict


#class ProfileCreate(BaseModel):
#    avatar_id: int
#    audio_reference_path: str
#    note: str | None = None
#    prompt_voice_clone_json: str


class ProfileResponse(BaseModel):
    id: int
    avatar_id: int
    audio_reference_path: str
    note: str | None
    prompt_voice_clone_json: str

    model_config = ConfigDict(from_attributes=True)