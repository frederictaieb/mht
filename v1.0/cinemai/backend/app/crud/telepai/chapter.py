# backend/app/crud/telepai/chapter.py
from sqlalchemy.orm import Session
from app.models.telepai.chapter import Chapter
from app.schemas.telepai.chapter import ChapterCreate


def create_chapter(chapter: ChapterCreate, db: Session):
    db_chapter = Chapter(chapter_number=chapter.chapter_number)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


def get_all_chapters(db: Session):
    return db.query(Chapter).all()


def get_chapter(chapter_id: int, db: Session):
    return db.query(Chapter).filter(Chapter.id == chapter_id).first()


def delete_chapter(chapter_id: int, db: Session):
    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if db_chapter is None:
        return None

    db.delete(db_chapter)
    db.commit()
    return db_chapter