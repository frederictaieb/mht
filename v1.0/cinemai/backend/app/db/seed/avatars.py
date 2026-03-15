import logging 
from sqlalchemy.orm import Session
from app.models.telepai.avatar import Avatar
from app.models.telepai.actress import Actress


AVATARS = [
    ("Bud", "Alice Preyssas"),
    ("Cassie", "Alice Preyssas"),
    ("Cillian", "Alexiane Torres"),
    ("Dutch", "Alexiane Torres"),
    ("Ed", "Camille Arrivé"),
    ("Morris", "Camille Arrivé"),
    ("Goldweiser", "Chloé Froget"),
    ("Tony", "Chloé Froget"),
    ("Francie", "Diane Renier"),
    ("Joe", "Diane Renier"),
    ("Ellen", "Hélène Boutin"),
    ("Émile", "Hélène Boutin"),
    ("Jim", "Julie Cavanna"),
    ("Georges", "Léna Bréban"),
    ("Jake", "Lymia Vitte"),
    ("Nellie", "Lymia Vitte"),
    ("Stan", "Lymia Vitte"),
    ("Anna", "Madison Golaz"),
    ("Émilie", "Madison Golaz"),
    ("Ogeltorpe", "Madison Golaz"),
]

logger = logging.getLogger(__name__)

def seed_avatars(db: Session) -> None:
    logger.info("Avatars")

    actresses = {
        a.name.lower(): a.id
        for a in db.query(Actress).all()
    }

    existing = {
        name.lower()
        for (name,) in db.query(Avatar.name).all()
    }

    for avatar_name, actress_name in AVATARS:

        avatar_name = avatar_name.strip().title()
        actress_id = actresses.get(actress_name.lower())

        if actress_id and avatar_name.lower() not in existing:
            db.add(
                Avatar(
                    name=avatar_name,
                    actress_id=actress_id
                )
            )