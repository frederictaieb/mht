# backend/app/crud/telepai/speech.py
from sqlalchemy.orm import Session
from app.models.telepai.speech import Speech
from app.schemas.telepai.speech import SpeechCreate
from app.models.telepai.presence import Presence

def create_speech(speech: SpeechCreate, db: Session):
    db_presence = db.query(Presence).filter(Presence.id == speech.presence_id).first()

    if db_presence is None:
        return None

    db_speech = Speech(
        presence_id=speech.presence_id,
        #title=speech.title
        title=f"{db_presence.avatar.name} : {db_presence.chapter.chapter_number}",
        conent=SpeechCreate.content
    )

    db.add(db_speech)
    db.commit()
    db.refresh(db_speech)

    return db_speech


def get_all_speeches(db: Session):
    return db.query(Speech).all()


def get_speech(speech_id: int, db: Session):
    return db.query(Speech).filter(Speech.id == speech_id).first()


def delete_speech(speech_id: int, db: Session):
    db_speech = db.query(Speech).filter(Speech.id == speech_id).first()

    if db_speech is None:
        return None

    db.delete(db_speech)
    db.commit()

    return db_speech