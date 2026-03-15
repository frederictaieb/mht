import logging
from sqlalchemy.orm import Session

from app.models.telepai.avatar import Avatar
from app.models.telepai.profile import Profile

logger = logging.getLogger(__name__)

PROFILES = [
    {
        "avatar_name": "Bud",
        "audio_reference_path": "app/data/voices/voices/avatars/bud/bud_colere.wav",
        "note": "bud-colere",
    },
]
        

def seed_profiles(db: Session) -> None:
    logger.info("Seeding profiles")

    avatars = {
        avatar.name.lower(): avatar.id
        for avatar in db.query(Avatar).all()
    }

    existing_profiles = {
        (profile.avatar_id, profile.audio_reference_path)
        for profile in db.query(Profile).all()
    }

    for item in PROFILES:
        avatar_name = item["avatar_name"].strip().title()
        avatar_id = avatars.get(avatar_name.lower())

        if not avatar_id:
            logger.warning(f"Avatar not found for profile: {avatar_name}")
            continue

        key = (avatar_id, item["audio_reference_path"])

        if key in existing_profiles:
            logger.info(f"Profile already exists for avatar: {avatar_name}")
            continue

        logger.info(f"Creating profile for avatar: {avatar_name}")

        db.add(
            Profile(
                avatar_id=avatar_id,
                audio_reference_path=item["audio_reference_path"],
                note=item.get("note"),
            )
        )

        existing_profiles.add(key)