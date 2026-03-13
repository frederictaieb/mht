# backend/app/services/telepai_services.py
import os

import torch
import soundfile as sf
from fastapi import HTTPException
from faster_whisper import WhisperModel
from qwen_tts import Qwen3TTSModel, VoiceClonePromptItem
from starlette.concurrency import run_in_threadpool

from dataclasses import dataclass, field


class TelepaiServices:
    def __init__(self) -> None:

        self.model_stt = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

        #self.model_qwen = Qwen3TTSModel.from_pretrained(
        #    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        #    device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        #    dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        #    attn_implementation="sdpa" if torch.cuda.is_available() else None,
        #)

        qwen_path = "/Users/fete/Desktop/code/mht/v1.0/cinemai/backend/app/data/ai_models/Qwen3-TTS-12Hz-1.7B-Base"

        qwen_kwargs = {
            "dtype": torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            "local_files_only": True,
        }

        if torch.cuda.is_available():
            qwen_kwargs["device_map"] = "cuda:0"
            qwen_kwargs["attn_implementation"] = "sdpa"

        self.model_qwen = Qwen3TTSModel.from_pretrained(
            qwen_path,
            **qwen_kwargs,
        )

        self.actresses: dict[str, "Actress"] = {}

    async def stt(self, file_path: str) -> str:
        try:
            if not file_path:
                raise HTTPException(status_code=400, detail="Aucun fichier fourni.")

            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail="Le fichier n'existe pas.")

            segments, info = await run_in_threadpool(
                lambda: self.model_stt.transcribe(file_path, beam_size=5)
            )

            result = " ".join(
                segment.text.strip()
                for segment in segments
                if getattr(segment, "text", None) and segment.text.strip()
            ).strip()

            return result

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur pendant la transcription : {e}",
            )

    async def create_voice_clone_prompt(
        self,
        ref_text: str,
        file_path: str
    ) -> list[VoiceClonePromptItem]:
        return await run_in_threadpool(
            lambda: self.model_qwen.create_voice_clone_prompt(
                ref_text=ref_text,
                ref_audio=file_path,
                x_vector_only_mode=False,
            )
        )

    async def generate_voice_clone(
        self,
        voice_clone_prompt: list[VoiceClonePromptItem],
        new_text: str,
        output_path: str = "output_voice_clone_1.wav"
    ) -> str:
        wavs, sr = await run_in_threadpool(
            lambda: self.model_qwen.generate_voice_clone(
                text=new_text,
                language="French",
                voice_clone_prompt=voice_clone_prompt,
            )
        )

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        await run_in_threadpool(lambda: sf.write(output_path, wavs[0], sr))
        return output_path
    
    async def create_actress(self, name: str, ref_audio_path: str) -> "Actress":
        actress = await Actress.create(
            name=name,
            default_ref_audio=ref_audio_path,
            telepai_service=self,
        )
        self.actresses[name] = actress
        return actress

    def get_actress(self, name: str) -> "Actress":
        actress = self.actresses.get(name)
        if actress is None:
            raise HTTPException(status_code=404, detail=f"Actrice '{name}' introuvable.")
        return actress


@dataclass
class Actress:
    name: str
    default_ref_audio: str
    telepai_service: TelepaiServices
    default_ref_text: str = ""
    default_voice_clone_prompt: list[VoiceClonePromptItem] | None = field(default=None)

    @classmethod
    async def create(
        cls,
        name: str,
        default_ref_audio: str,
        telepai_service: TelepaiServices
    ) -> "Actress":
        self = cls(
            name=name,
            default_ref_audio=default_ref_audio,
            telepai_service=telepai_service,
        )

        self.default_ref_text = await telepai_service.stt(default_ref_audio)

        self.default_voice_clone_prompt = await telepai_service.create_voice_clone_prompt(
            self.default_ref_text,
            default_ref_audio,
        )

        return self

    async def say(self, new_text: str) -> str:
        if self.default_voice_clone_prompt is None:
            raise ValueError("default_voice_clone_prompt is missing")

        output_path = os.path.join("app/data/telepai/output", f"{self.name}_voice_clone.wav")

        return await self.telepai_service.generate_voice_clone(
            voice_clone_prompt=self.default_voice_clone_prompt,
            new_text=new_text,
            output_path=output_path,
        )