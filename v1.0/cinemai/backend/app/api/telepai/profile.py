# backend/app/api/routes/telepai/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.profile import ProfileCreate, ProfileResponse
from app.crud.telepai.profile import (
    create_profile,
    get_all_profiles,
    get_profile,
    delete_profile
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=ProfileResponse)
def create(profile: ProfileCreate, db: Session = Depends(get_db)):

    db_profile = create_profile(profile, db)

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Avatar not found")

    return db_profile


@router.get("/", response_model=list[ProfileResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_profiles(db)


@router.get("/{profile_id}", response_model=ProfileResponse)
def get(profile_id: int, db: Session = Depends(get_db)):

    db_profile = get_profile(profile_id, db)

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_profile


@router.delete("/{profile_id}")
def delete(profile_id: int, db: Session = Depends(get_db)):

    db_profile = delete_profile(profile_id, db)

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile deleted"}