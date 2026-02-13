from fastapi import FastAPI
from app.api.routes.faceswap import router as faceswap_router

app = FastAPI()
app.include_router(faceswap_router)
