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

class CharacterWithActress(BaseModel):
    character: str
    actress: str

class SceneCharacter(BaseModel):
    scene_number: int
    character: str
    actress: str

class ActressScene(BaseModel):
    actress: str
    character: str
    scene_number: int

class SceneCount(BaseModel):
    scene_number: int
    nb_characters: int


class ActressSceneCount(BaseModel):
    actress: str
    nb_scenes: int

class VoiceProfileCreateRequest(BaseModel):
    avatar_name: str
    ref_audio_path: str
    note: str | None = None

class MonologueCreateRequest(BaseModel):
    scene_number: int
    title: str | None = None

class MonologueLineCreateRequest(BaseModel):
    monologue_id: int
    voice_profile_id: int
    line_order: int
    text: str
    generation_note: str | None = None

class GenerateMonologueLineAudioRequest(BaseModel):
    monologue_line_id: int
    output_dir: str | None = "app/data/generated_audio"


### NOUVEAU


class ActressCreate(BaseModel):
    name: str


class ActressResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True