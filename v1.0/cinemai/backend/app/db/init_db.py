import logging

# backend/app/db/init_db.py
from app.db.database import Base, engine, SessionLocal

# Importer tous les modèles pour que SQLAlchemy les enregistre
from app.models.telepai.actress import Actress
from app.models.telepai.avatar import Avatar
from app.models.telepai.chapter import Chapter
from app.models.telepai.presence import Presence
from app.models.telepai.profile import Profile
from app.models.telepai.speech import Speech
from app.models.telepai.line import Line

from app.db.seed.actresses import seed_actresses 
from app.db.seed.avatars import seed_avatars
from app.db.seed.chapters import seed_chapters 
from app.db.seed.presences import seed_presences
from app.db.seed.speeches import seed_speeches
from app.db.seed.lines import seed_lines
from app.db.seed.profiles import seed_profiles

logger = logging.getLogger(__name__)

def create_tables() -> None:
    logger.info("Creating tables")
    Base.metadata.create_all(bind=engine)


def seed_data() -> None:
    logger.info("Seeding tables")
    db = SessionLocal()
    try:
        
        seed_actresses(db)
        db.flush()

        seed_avatars(db)
        db.flush()

        seed_chapters(db)
        db.flush()

        seed_profiles(db)
        db.flush()

        seed_presences(db)
        db.flush()

        seed_speeches(db)
        db.flush()

        seed_lines(db)
        db.flush()

        #logger.info("Seeding Speeches")
        #logger.info("Seeding Lines")
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    create_tables()
    seed_data()