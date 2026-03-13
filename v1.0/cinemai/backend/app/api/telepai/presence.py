# backend/app/api/routes/telepai/presence.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.presence import PresenceCreate, PresenceResponse
from app.crud.telepai.presence import (
    create_presence as crud_create_presence,
    get_all_presences as crud_get_all_presences,
    get_presence as crud_get_presence,
    delete_presence as crud_delete_presence,
)

router = APIRouter(prefix="/presence", tags=["Presence"])


@router.post("/", response_model=PresenceResponse)
def create_presence(presence: PresenceCreate, db: Session = Depends(get_db)):
    db_presence, error = crud_create_presence(presence, db)

    if error == "chapter_not_found":
        raise HTTPException(status_code=404, detail="Chapter not found")
    if error == "avatar_not_found":
        raise HTTPException(status_code=404, detail="Avatar not found")
    if error == "already_exists":
        raise HTTPException(status_code=400, detail="Presence already exists")

    return db_presence


@router.get("/", response_model=list[PresenceResponse])
def get_all_presences(db: Session = Depends(get_db)):
    return crud_get_all_presences(db)


@router.get("/{presence_id}", response_model=PresenceResponse)
def get_presence(presence_id: int, db: Session = Depends(get_db)):
    db_presence = crud_get_presence(presence_id, db)

    if db_presence is None:
        raise HTTPException(status_code=404, detail="Presence not found")

    return db_presence


@router.delete("/{presence_id}")
def delete_presence(presence_id: int, db: Session = Depends(get_db)):
    db_presence = crud_delete_presence(presence_id, db)

    if db_presence is None:
        raise HTTPException(status_code=404, detail="Presence not found")

    return {"message": "Presence deleted"}