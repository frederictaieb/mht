from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.avatar import AvatarCreate, AvatarResponse

from app.crud.telepai.avatar import (
    create_avatar as crud_create_avatar,
    get_all_avatars as crud_get_all_avatars,
    get_avatar_by_id as crud_get_avatar_by_id,
    delete_avatar as crud_delete_avatar,
)

router = APIRouter(prefix="/avatar", tags=["Avatar"])

@router.post("/", response_model=AvatarResponse)
def create_avatar(avatar: AvatarCreate, db: Session = Depends(get_db)):
    return crud_create_avatar(avatar, db)


@router.get("/", response_model=list[AvatarResponse])
def get_all_avatars(db: Session = Depends(get_db)):
    return crud_get_all_avatars(db)


@router.get("/{avatar_id}", response_model=AvatarResponse)
def get_avatar(avatar_id: int, db: Session = Depends(get_db)):
    db_avatar = crud_get_avatar_by_id(avatar_id, db)

    if db_avatar is None:
        raise HTTPException(status_code=404, detail="Avatar not found")

    return db_avatar


@router.delete("/{avatar_id}")
def delete_avatar(avatar_id: int, db: Session = Depends(get_db)):
    db_avatar = crud_delete_avatar(avatar_id, db)

    if db_avatar is None:
        raise HTTPException(status_code=404, detail="Avatar not found")

    return {"message": f"Avatar {db_avatar.name} deleted successfully"}