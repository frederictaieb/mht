import logging 
from sqlalchemy.orm import Session
from app.models.telepai.chapter import Chapter
from app.models.telepai.avatar import Avatar
from app.models.telepai.presence import Presence


PRESENCES = [
    (1, "Bud"),
    (2, "Bud"),
    (5, "Bud"),

    (2, "Cassie"),
    (3, "Cassie"),
    (4, "Cassie"),

    (1, "Cillian"),
    (2, "Cillian"),
    (4, "Cillian"),

    (4, "Dutch"),
    (4, "Dutch"),
    (5, "Dutch"),

    (2, "Ed"),
    (3, "Ed"),
    (5, "Ed"),

    (2, "Morris"),
    (3, "Morris"),
    (4, "Morris"),

    (1, "Goldweiser"),
    (3, "Goldweiser"),
    (4, "Goldweiser"),

    (2, "Tony"),
    (4, "Tony"),
    (5, "Tony"),

    (2, "Francie"),
    (3, "Francie"),
    (4, "Francie"),

    (1, "Joe"),
    (3, "Joe"),
    (5, "Joe"),

    (2, "Ellen"),
    (4, "Ellen"),
    (5, "Ellen"),

    (1, "Émile"),
    (4, "Émile"),
    (5, "Émile"),

    (2, "Jim"),
    (3, "Jim"),
    (4, "Jim"),

    (1, "Georges"),
    (2, "Georges"),
    (5, "Georges"),

    (1, "Jake"),
    (2, "Jake"),
    (5, "Jake"),

    (1, "Nellie"),
    (3, "Nellie"),
    (5, "Nellie"),

    (2, "Stan"),
    (3, "Stan"),
    (4, "Stan"),

    (3, "Anna"),
    (4, "Anna"),
    (5, "Anna"),

    (3, "Émilie"),

    (1, "Ogeltorpe"),
    (2, "Ogeltorpe"),
    (4, "Ogeltorpe"),
]

logger = logging.getLogger(__name__)

def seed_presences(db: Session) -> None:
    logger.info("Presences")
    chapters = {
        chapter.chapter_number: chapter.id
        for chapter in db.query(Chapter).all()
    }

    avatars = {
        avatar.name.strip().lower(): avatar.id
        for avatar in db.query(Avatar).all()
    }

    existing = {
        (chapter_id, avatar_id)
        for chapter_id, avatar_id in db.query(
            Presence.chapter_id,
            Presence.avatar_id,
        ).all()
    }

    for chapter_number, avatar_name in PRESENCES:
        chapter_id = chapters.get(chapter_number)
        avatar_id = avatars.get(avatar_name.strip().lower())

        if chapter_id and avatar_id and (chapter_id, avatar_id) not in existing:
            db.add(
                Presence(
                    chapter_id=chapter_id,
                    avatar_id=avatar_id,
                )
            )