# backend/app/api/routes/telepai/actress.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.actress import ActressCreate, ActressResponse

from app.crud.telepai.actress import create_actress as crud_create_actress
from app.crud.telepai.actress import get_all_actresses as crud_get_all_actresses
from app.crud.telepai.actress import delete_actress as crud_delete_actress
from app.crud.telepai.actress import get_actress as crud_get_actress

router = APIRouter(prefix="/actress", tags=["Actress"])

@router.post("/actress/create", response_model=ActressCreate)
def create_actress(actress: ActressCreate, db: Session = Depends(get_db)):
    return crud_create_actress(actress, db)


@router.get("/actress/all", response_model=list[ActressResponse])
def get_all_actresses(db: Session = Depends(get_db)):
    return crud_get_all_actresses(db)
#    return db.query(Actress).all()

@router.delete("/actress/delete/{actress_id}")
def delete_actress(actress_id: int, db: Session = Depends(get_db)):
    return crud_delete_actress(actress_id, db)

@router.get("/actress/{actress_id}", response_model=ActressResponse)
def get_actress(actress_id: int, db: Session = Depends(get_db)):
    return crud_get_actress(actress_id, db)