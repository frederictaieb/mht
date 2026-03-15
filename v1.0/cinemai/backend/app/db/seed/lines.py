import logging
from sqlalchemy.orm import Session

from app.models.telepai.speech import Speech
from app.models.telepai.line import Line

logger = logging.getLogger(__name__)


def seed_lines(db: Session) -> None:
    logger.info("Seeding lines")

    speeches = db.query(Speech).all()

    for speech in speeches:

        if not speech.content:
            continue

        lines = speech.content.split("\n")

        for line in lines:
            text = line.strip()

            if not text:
                continue

            db.add(
                Line(
                    speech_id=speech.id,
                    content=text
                )
            )