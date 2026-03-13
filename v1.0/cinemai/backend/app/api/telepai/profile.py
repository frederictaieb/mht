# backend/app/api/routes/telepai/profile.py
#from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session

#from app.db.session import get_db
#from app.schemas.telepai.profile import ProfileCreate, ProfileResponse
#from app.crud.telepai.profile import (
#    create_profile,
#    get_all_profiles,
#    get_profile,
#    delete_profile
#)

import json
import os
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telepai.profile import ProfileResponse
from app.crud.telepai.profile import (
    create_profile as crud_create_profile,
    get_all_profiles as crud_get_all_profiles,
    get_profile as crud_get_profile,
    delete_profile as crud_delete_profile
)

from app.services.telepai_services import TelepaiServices
from app.utils.serializers import serialize_voice_clone_prompt_item

router = APIRouter(prefix="/profile", tags=["Profile"])

##########
logger = logging.getLogger(__name__)
UPLOAD_DIR = "app/data/telepai/input"
telepai_service = TelepaiServices()


@router.post("/", response_model=ProfileResponse)
async def create(
    avatar_id: int = Form(...),
    note: str | None = Form(None),
    ref_text: str | None = Form(None),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    logger.info("Upload directory created")

    if not audio_file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier audio fourni.")

    ext = os.path.splitext(audio_file.filename)[1].lower()
    allowed_exts = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}

    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté. Formats autorisés : {', '.join(sorted(allowed_exts))}"
        )

    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    logger.info(f"filepath: {file_path}")

    try:
        content = await audio_file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'enregistrement du fichier audio : {e}"
        )

    try:
        # Si le texte n'est pas fourni, on le déduit avec STT
        final_ref_text = ref_text.strip() if ref_text and ref_text.strip() else None

        logger.info(f"ref_text:{final_ref_text}")

        if final_ref_text is None:
            logger.info("stt")
            final_ref_text = await telepai_service.stt(file_path)

        logger.info("create_voice_clone_prompt")
        voice_clone_prompt = await telepai_service.create_voice_clone_prompt(
            ref_text=final_ref_text,
            file_path=file_path,
        )

        # Sérialisation JSON pour stockage BDD
        logger.info("prompt_voice_clone_json")
        prompt_voice_clone_json = json.dumps(
            [serialize_voice_clone_prompt_item(item) for item in voice_clone_prompt],
            ensure_ascii=False
        )

        logger.info("crud_create_profile")
        db_profile = crud_create_profile(
            avatar_id=avatar_id,
            audio_reference_path=file_path,
            note=note,
            prompt_voice_clone_json=prompt_voice_clone_json,
            db=db,
        )

        if db_profile is None:
            raise HTTPException(status_code=404, detail="Avatar not found")

        return db_profile

    except HTTPException:
        # On peut supprimer le fichier si besoin en cas d'erreur métier
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la création du profile : {e}"
        )

##########

#@router.post("/", response_model=ProfileResponse)
#def create(profile: ProfileCreate, db: Session = Depends(get_db)):

#    db_profile = create_profile(profile, db)

#    if db_profile is None:
#        raise HTTPException(status_code=404, detail="Avatar not found")

#    return db_profile


@router.get("/all", response_model=list[ProfileResponse])
def get_all_profiles(db: Session = Depends(get_db)):
    return crud_get_all_profiles(db)


@router.get("/{profile_id}", response_model=ProfileResponse)
def get(profile_id: int, db: Session = Depends(get_db)):

    db_profile = crud_get_profile(profile_id, db)

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_profile


#@router.delete("/{profile_id}")
#def delete(profile_id: int, db: Session = Depends(get_db)):

#    db_profile = crud_delete_profile(profile_id, db)

#    if db_profile is None:
#        raise HTTPException(status_code=404, detail="Profile not found")

#    return {"message": "Profile deleted"}

@router.delete("/{profile_id}")
def delete(profile_id: int, db: Session = Depends(get_db)):

    db_profile = crud_get_profile(profile_id, db)

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    audio_path = db_profile.audio_reference_path

    # suppression en base
    crud_delete_profile(profile_id, db)

    # suppression fichier audio
    try:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Audio file deleted: {audio_path}")
    except Exception as e:
        logger.warning(f"Impossible de supprimer le fichier audio: {e}")

    return {"message": "Profile deleted"}