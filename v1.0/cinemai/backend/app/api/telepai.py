from fastapi import APIRouter, UploadFile, File
import tempfile

import torch
import soundfile as sf

from faster_whisper import WhisperModel
from qwen_tts import Qwen3TTSModel

from pydantic import BaseModel
from app.services.telepai_services import TelepaiServices

telepai_router = APIRouter(prefix="/telepai", tags=["telepai"])
telepai_services = TelepaiServices()

JOY = "Voix française joyeuse, lumineuse, souriante, expressive, naturelle."
TRISTE = "Voix française triste, douce, lente, fragile, avec beaucoup d'émotion."
COLERE = "Voix française ferme, nerveuse, plus rapide, avec une colère contenue."
DOCU = "Voix française style documentaire, posée, claire, profonde, articulée."
PODCAST = "Voix française style podcast intime, calme, proche, naturelle."
MEDITATION = "Voix française très calme, lente, rassurante, presque chuchotée."

MODEL_NAME = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

model_qwen = Qwen3TTSModel.from_pretrained(
    MODEL_NAME,
    device_map=device,
    dtype=dtype,
    attn_implementation="sdpa" if torch.cuda.is_available() else None,
)

@telepai_router.post("/stt")
async def stt(file: UploadFile = File(...)):
    return await telepai_services.stt(file)




