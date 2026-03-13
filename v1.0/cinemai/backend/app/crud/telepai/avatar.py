from sqlalchemy.orm import Session
from app.models.telepai.avatar import Avatar
from app.schemas.telepai.avatar import AvatarCreate


def create_avatar(avatar: AvatarCreate, db: Session):
    db_avatar = Avatar(
        name=avatar.name,
        actress_id=avatar.actress_id
    )
    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)
    return db_avatar


def get_all_avatars(db: Session):
    return db.query(Avatar).all()


def get_avatar_by_id(avatar_id: int, db: Session):
    return db.query(Avatar).filter(Avatar.id == avatar_id).first()


def delete_avatar(avatar_id: int, db: Session):
    db_avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()

    if db_avatar is None:
        return None

    db.delete(db_avatar)
    db.commit()
    return db_avatar