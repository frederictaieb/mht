import logging 
from sqlalchemy.orm import Session
from app.models.telepai.chapter import Chapter


CHAPTERS = [1, 2, 3, 4, 5]

logger = logging.getLogger(__name__)

def seed_chapters(db: Session) -> None:
    logger.info("Chapters")
    existing = {
        number for (number,) in db.query(Chapter.chapter_number).all()
    }

    for number in CHAPTERS:
        if number not in existing:
            db.add(Chapter(chapter_number=number))