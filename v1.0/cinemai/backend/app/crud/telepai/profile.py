# backend/app/crud/telepai/profile.py
from sqlalchemy.orm import Session
from app.models.telepai.avatar import Avatar
from app.models.telepai.profile import Profile
from app.schemas.telepai.profile import ProfileCreate


def create_profile(profile: ProfileCreate, db: Session):

    avatar = db.query(Avatar).filter(Avatar.id == profile.avatar_id).first()

    if avatar is None:
        return None

    db_profile = Profile(
        avatar_id=profile.avatar_id,
        audio_reference_path=profile.audio_reference_path,
        note=profile.note,
        prompt_voice_clone_json=profile.prompt_voice_clone_json
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


def get_all_profiles(db: Session):
    return db.query(Profile).all()


def get_profile(profile_id: int, db: Session):
    return db.query(Profile).filter(Profile.id == profile_id).first()


def delete_profile(profile_id: int, db: Session):

    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if db_profile is None:
        return None

    db.delete(db_profile)
    db.commit()

    return db_profile