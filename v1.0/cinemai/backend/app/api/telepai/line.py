# backend/app/api/routes/telepai/line.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.line import LineCreate, LineResponse
from app.crud.telepai.line import (
    create_line as crud_create_line,
    get_all_lines as crud_get_all_lines,
    get_line as crud_get_line,
    delete_line as crud_delete_line,
)

router = APIRouter(prefix="/lines", tags=["Lines"])


@router.post("/", response_model=LineResponse)
def create_line(line: LineCreate, db: Session = Depends(get_db)):
    db_line, error = crud_create_line(line, db)

    if error == "speech_not_found":
        raise HTTPException(status_code=404, detail="Speech not found")
    if error == "profile_not_found":
        raise HTTPException(status_code=404, detail="Profile not found")
    if error == "line_order_exists":
        raise HTTPException(status_code=400, detail="This line_order already exists for this speech")

    return db_line


@router.get("/", response_model=list[LineResponse])
def get_all_lines(db: Session = Depends(get_db)):
    return crud_get_all_lines(db)


@router.get("/{line_id}", response_model=LineResponse)
def get_line(line_id: int, db: Session = Depends(get_db)):
    db_line = crud_get_line(line_id, db)

    if db_line is None:
        raise HTTPException(status_code=404, detail="Line not found")

    return db_line


@router.delete("/{line_id}")
def delete_line(line_id: int, db: Session = Depends(get_db)):
    db_line = crud_delete_line(line_id, db)

    if db_line is None:
        raise HTTPException(status_code=404, detail="Line not found")

    return {"message": "Line deleted"}