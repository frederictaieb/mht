# backend/app/crud/telepai/actress.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.telepai.actress import Actress
from app.schemas.telepai.actress import ActressCreate
from app.db.session import get_db

def create_actress(actress: ActressCreate, db: Session = Depends(get_db)):
    db_actress = Actress(name=actress.name.lower())
    db.add(db_actress)
    db.commit()
    db.refresh(db_actress)
    return db_actress


def get_all_actresses(db: Session = Depends(get_db)):
    return db.query(Actress).all()


def delete_actress(actress_id: int, db: Session = Depends(get_db)):
    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

    if db_actress is None:
        raise HTTPException(status_code=404, detail="Actress not found")
        
    db.delete(db_actress)
    db.commit()
    return {"message": "Actress deleted successfully"}


def get_actress(actress_id: int, db: Session = Depends(get_db)):
    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

    if db_actress is None:
        raise HTTPException(status_code=404, detail="Actress not found")
    
    return db_actress