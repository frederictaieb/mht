# backend/app/services/telepai_services.py

import json
import os
from dataclasses import asdict, is_dataclass

import soundfile as sf
import torch
from fastapi import HTTPException
from faster_whisper import WhisperModel
from qwen_tts import Qwen3TTSModel, VoiceClonePromptItem
from starlette.concurrency import run_in_threadpool

from app.services.database_services import DatabaseServices


def serialize_prompt_items(prompt_items: list) -> str:
    result = []

    for item in prompt_items:
        if hasattr(item, "model_dump"):
            result.append(item.model_dump())
        elif is_dataclass(item):
            result.append(asdict(item))
        elif hasattr(item, "__dict__"):
            result.append(vars(item))
        else:
            result.append(str(item))

    return json.dumps(result, ensure_ascii=False)


def deserialize_prompt_items(prompt_json: str) -> list[VoiceClonePromptItem]:
    raw_items = json.loads(prompt_json)
    result = []

    for item in raw_items:
        if isinstance(item, dict):
            result.append(VoiceClonePromptItem(**item))
        else:
            raise ValueError("Format JSON invalide pour VoiceClonePromptItem.")

    return result


class TelepaiServices:
    def __init__(self, db_services: DatabaseServices) -> None:
        self.db_services = db_services

        self.model_stt = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

        self.model_qwen = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            device_map="cuda:0" if torch.cuda.is_available() else "cpu",
            dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            attn_implementation="sdpa" if torch.cuda.is_available() else None,
        )

    async def stt(self, file_path: str) -> str:
        try:
            if not file_path:
                raise HTTPException(status_code=400, detail="Aucun fichier fourni.")

            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail="Le fichier n'existe pas.")

            segments, _info = await run_in_threadpool(
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
        file_path: str,
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
        output_path: str = "output_voice_clone_1.wav",
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

    async def create_voice_profile_from_avatar_name(
        self,
        avatar_name: str,
        ref_audio_path: str,
        note: str | None = None,
    ) -> dict:
        avatar = self.db_services.get_avatar_by_name(avatar_name)
        if avatar is None:
            raise HTTPException(
                status_code=404,
                detail=f"Avatar '{avatar_name}' introuvable.",
            )

        if not os.path.isfile(ref_audio_path):
            raise HTTPException(
                status_code=404,
                detail=f"Le fichier '{ref_audio_path}' n'existe pas.",
            )

        ref_text = await self.stt(ref_audio_path)
        prompt_items = await self.create_voice_clone_prompt(ref_text, ref_audio_path)
        prompt_json = serialize_prompt_items(prompt_items)

        voice_profile_id = self.db_services.create_voice_profile(
            avatar_id=avatar["id"],
            audio_reference_path=ref_audio_path,
            note=note,
            prompt_voice_clone_json=prompt_json,
        )

        return {
            "id": voice_profile_id,
            "avatar_id": avatar["id"],
            "avatar_name": avatar["name"],
            "audio_reference_path": ref_audio_path,
            "note": note,
            "ref_text": ref_text,
        }

    async def create_monologue_for_scene_number(
        self,
        scene_number: int,
        title: str | None = None,
    ) -> dict:
        scene = self.db_service.get_scene_by_number(scene_number)
        if scene is None:
            raise HTTPException(
                status_code=404,
                detail=f"Scène '{scene_number}' introuvable.",
            )

        monologue_id = self.db_service.create_monologue(
            scene_id=scene["id"],
            title=title,
        )

        return {
            "id": monologue_id,
            "scene_id": scene["id"],
            "scene_number": scene["scene_number"],
            "title": title,
        }

    async def create_monologue_line(
        self,
        monologue_id: int,
        voice_profile_id: int,
        line_order: int,
        text: str,
        generation_note: str | None = None,
    ) -> dict:
        monologue = self.db_service.get_monologue_by_id(monologue_id)
        if monologue is None:
            raise HTTPException(
                status_code=404,
                detail=f"Monologue '{monologue_id}' introuvable.",
            )

        voice_profile = self.db_service.get_voice_profile_by_id(voice_profile_id)
        if voice_profile is None:
            raise HTTPException(
                status_code=404,
                detail=f"Voice profile '{voice_profile_id}' introuvable.",
            )

        line_id = self.db_service.create_monologue_line(
            monologue_id=monologue_id,
            voice_profile_id=voice_profile_id,
            line_order=line_order,
            text=text,
            generation_note=generation_note,
        )

        return {
            "id": line_id,
            "monologue_id": monologue_id,
            "voice_profile_id": voice_profile_id,
            "line_order": line_order,
            "text": text,
            "generation_note": generation_note,
        }

    async def generate_audio_for_monologue_line(
        self,
        monologue_line_id: int,
        output_dir: str = "app/data/generated_audio",
    ) -> dict:
        line = self.db_service.get_monologue_line_by_id(monologue_line_id)
        if line is None:
            raise HTTPException(
                status_code=404,
                detail=f"Ligne '{monologue_line_id}' introuvable.",
            )

        voice_profile = self.db_service.get_voice_profile_by_id(line["voice_profile_id"])
        if voice_profile is None:
            raise HTTPException(
                status_code=404,
                detail="Voice profile associé introuvable.",
            )

        try:
            prompt_items = deserialize_prompt_items(
                voice_profile["prompt_voice_clone_json"]
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Impossible de relire le prompt_voice_clone_json : {e}",
            )

        safe_avatar_name = line["avatar_name"].replace(" ", "_")
        filename = f"line_{monologue_line_id}_{safe_avatar_name}.wav"
        output_path = os.path.join(output_dir, filename)

        generated_path = await self.generate_voice_clone(
            voice_clone_prompt=prompt_items,
            new_text=line["text"],
            output_path=output_path,
        )

        self.db_service.update_monologue_line_audio_path(
            line_id=monologue_line_id,
            audio_path=generated_path,
        )

        return {
            "monologue_line_id": monologue_line_id,
            "audio_path": generated_path,
        }