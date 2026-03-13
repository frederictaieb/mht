# backend/app/api/routes/telepai.py
import os
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse

from app.services.telepai_services import TelepaiServices
from app.db.session import get_db

from app.schemas.telepai import (
    ActressCreate,
    CreateActressResponse,
    SayRequest,
    SayResponse,
)

from sqlalchemy.orm import Session
from app.models.telepai import Actress
from app.schemas.telepai import ActressResponse

telepai_router = APIRouter(prefix="/telepai", tags=["telepai"])
telepai_service = TelepaiServices()

#@telepai_router.post("/create_actress", response_model=CreateActressResponse)
#async def create_actress_old(name: str = Form(...), file: UploadFile = File(...)):
#    os.makedirs("app/data/telepai/input", exist_ok=True)
#    safe_filename = f"{name}_{file.filename}"
#    file_path = os.path.join("app/data/telepai/input", safe_filename)

#    with open(file_path, "wb") as buffer:
#        shutil.copyfileobj(file.file, buffer)

#    actress = await telepai_service.create_actress(name=name, ref_audio_path=file_path)

#    return CreateActressResponse(
#        name=actress.name,
#        ref_audio=actress.default_ref_audio,
#        ref_text=actress.default_ref_text,
#    )


#@telepai_router.post("/{name}/say", response_model=SayResponse)
#async def actress_say_old(name: str, text: str = Form(...)):
#    actress = telepai_service.get_actress(name)
#    file_path = await actress.say(text)

#    return SayResponse(
#        actress_name=name,
#        file_path=file_path,
#        audio_url=f"/telepai/{name}/get"
#    )


#@telepai_router.get("/{name}/get")
#async def get_actress_audio_old(name: str):
#    actress = telepai_service.get_actress(name)
#    output_path = os.path.join("app/data/telepai/output", f"{actress.name}_voice_clone.wav")

#    if not os.path.exists(output_path):
#        raise HTTPException(
#            status_code=404,
#            detail="Aucun fichier audio généré pour cette actrice."
#        )

#    return FileResponse(
#        path=output_path,
#        media_type="audio/wav",
#        filename=f"{actress.name}_voice_clone.wav",
#    )

###

#@telepai_router.post("/actress/create", response_model=ActressCreate)
#def create_actress(actress: ActressCreate, db: Session = Depends(get_db)):
#    db_actress = Actress(name=actress.name)
#    db.add(db_actress)
#    db.commit()
#    db.refresh(db_actress)
#    return db_actress

#@telepai_router.get("/actress/all", response_model=list[ActressResponse])
#def get_all_actresses(db: Session = Depends(get_db)):
#    return db.query(Actress).all()

#@telepai_router.delete("/actress/delete/{actress_id}")
#def delete_actress(actress_id: int, db: Session = Depends(get_db)):
#    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

#    if db_actress is None:
#        raise HTTPException(status_code=404, detail="Actress not found")
        
#    db.delete(db_actress)
#    db.commit()
#    return {"message": "Actress deleted successfully"}

#@telepai_router.get("/actress/{actress_id}", response_model=ActressResponse)
#def get_actress(actress_id: int, db: Session = Depends(get_db)):
#    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

#    if db_actress is None:
#        raise HTTPException(status_code=404, detail="Actress not found")
    
#    return db_actress


#@telepai_router.get("/actresses", response_model=list[ActressResponse])
#def get_all_actresses(db: Session = Depends(get_db)):
#    return db.query(Actress).all()


#@telepai_router.delete("/actresses/{actress_id}")
#def delete_actress(actress_id: int, db: Session = Depends(get_db)):
#    db_actress = db.query(Actress).filter(Actress.id == actress_id).first()

#    if db_actress is None:
#        raise HTTPException(status_code=404, detail="Actress not found")

#    db.delete(db_actress)
#    db.commit()

#    return {"message": "Actress deleted successfully"}