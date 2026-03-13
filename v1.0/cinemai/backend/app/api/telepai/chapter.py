# backend/app/api/routes/telepai/chapter.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.chapter import ChapterCreate, ChapterResponse
from app.crud.telepai.chapter import (
    create_chapter,
    get_all_chapters,
    get_chapter,
    delete_chapter
)

router = APIRouter(prefix="/chapter", tags=["Chapter"])


@router.post("/", response_model=ChapterResponse)
def create(chapter: ChapterCreate, db: Session = Depends(get_db)):
    return create_chapter(chapter, db)


@router.get("/", response_model=list[ChapterResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_chapters(db)


@router.get("/{chapter_id}", response_model=ChapterResponse)
def get(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = get_chapter(chapter_id, db)

    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return db_chapter


@router.delete("/{chapter_id}")
def delete(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = delete_chapter(chapter_id, db)

    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return {"message": "Chapter deleted"}