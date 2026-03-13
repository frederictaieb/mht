from pydantic import BaseModel, ConfigDict

class ChapterCreate(BaseModel):
    chapter_number: int


class ChapterResponse(BaseModel):
    id: int
    chapter_number: int

    model_config = ConfigDict(from_attributes=True)