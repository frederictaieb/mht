from pydantic import BaseModel, ConfigDict

class ActressCreate(BaseModel):
    name: str

class ActressResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
