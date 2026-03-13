# backend/app/crud/telepai/presence.py
from sqlalchemy.orm import Session
from app.models.telepai.presence import Presence
from app.models.telepai.chapter import Chapter
from app.models.telepai.avatar import Avatar

from app.schemas.telepai.presence import PresenceCreate


def create_presence(presence: PresenceCreate, db: Session):
    chapter = db.query(Chapter).filter(Chapter.chapter_number == presence.chapter_id).first()
    if chapter is None:
        return None, "chapter_not_found"

    avatar = db.query(Avatar).filter(Avatar.id == presence.avatar_id).first()
    if avatar is None:
        return None, "avatar_not_found"

    existing = db.query(Presence).filter(
        Presence.chapter_id == presence.chapter_id,
        Presence.avatar_id == presence.avatar_id
    ).first()

    if existing is not None:
        return None, "already_exists"

    db_presence = Presence(
        chapter_id=presence.chapter_id,
        avatar_id=presence.avatar_id
    )
    db.add(db_presence)
    db.commit()
    db.refresh(db_presence)
    return db_presence, None


def get_all_presences(db: Session):
    return db.query(Presence).all()


def get_presence(presence_id: int, db: Session):
    return db.query(Presence).filter(Presence.id == presence_id).first()


def delete_presence(presence_id: int, db: Session):
    db_presence = db.query(Presence).filter(Presence.id == presence_id).first()

    if db_presence is None:
        return None

    db.delete(db_presence)
    db.commit()
    return db_presence