from fastapi import APIRouter

from app.api.telepai.actress import router as actress_router
from app.api.telepai.avatar import router as avatar_router
from app.api.telepai.profile import router as profile_router

from app.api.telepai.chapter import router as chapter_router
from app.api.telepai.presence import router as presence_router

from app.api.telepai.speech import router as speech_router
from app.api.telepai.line import router as line_router


#from app.api.telepai.profile import router as profile_router

telepai_router = APIRouter(prefix="/telepai")

telepai_router.include_router(actress_router)
telepai_router.include_router(avatar_router)
telepai_router.include_router(profile_router)
telepai_router.include_router(chapter_router)
telepai_router.include_router(presence_router)
telepai_router.include_router(speech_router)
telepai_router.include_router(line_router)
