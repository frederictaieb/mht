# backend/app/api/routes/telepai/speech.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.speech import SpeechCreate, SpeechResponse
from app.crud.telepai.speech import (
    create_speech as crud_create_speech,
    get_all_speeches as crud_get_all_speeches,
    get_speech as crud_get_speech,
    delete_speech as crud_delete_speech,
)

router = APIRouter(prefix="/speeches", tags=["Speeches"])


@router.post("/", response_model=SpeechResponse)
def create_speech(speech: SpeechCreate, db: Session = Depends(get_db)):
    db_speech = crud_create_speech(speech, db)

    if db_speech is None:
        raise HTTPException(status_code=404, detail="Presence not found")

    return db_speech


@router.get("/all", response_model=list[SpeechResponse])
def get_all_speeches(db: Session = Depends(get_db)):
    return crud_get_all_speeches(db)


@router.get("/{speech_id}", response_model=SpeechResponse)
def get_speech(speech_id: int, db: Session = Depends(get_db)):
    db_speech = crud_get_speech(speech_id, db)

    if db_speech is None:
        raise HTTPException(status_code=404, detail="Speech not found")

    return db_speech


@router.delete("/{speech_id}")
def delete_speech(speech_id: int, db: Session = Depends(get_db)):
    db_speech = crud_delete_speech(speech_id, db)

    if db_speech is None:
        raise HTTPException(status_code=404, detail="Speech not found")

    return {"message": "Speech deleted"}