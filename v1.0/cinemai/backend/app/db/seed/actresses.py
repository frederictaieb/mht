# backend/app/db/seed/actresses.py
import logging
from sqlalchemy.orm import Session
from app.models.telepai.actress import Actress




ACTRESS_NAMES = [
    "Alice Preyssas",
    "Alexiane Torres",
    "Camille Arrivé",
    "Chloé Froget",
    "Diane Renier",
    "Hélène Boutin",
    "Julie Cavanna",
    "Lymia Vitte",
    "Madison Golaz",
    "Léna Bréban",
]

logger = logging.getLogger(__name__)

def seed_actresses(db: Session) -> None:
    logger.info("Actresses")
    existing_names = {name.lower() for (name,) in db.query(Actress.name).all()}

    for name in ACTRESS_NAMES:
        formatted_name = name.title()

        if formatted_name.lower() not in existing_names:
            db.add(Actress(name=formatted_name))