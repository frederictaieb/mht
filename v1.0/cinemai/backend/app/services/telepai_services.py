
from faster_whisper import WhisperModel
from fastapi import UploadFile
import tempfile

class TelepaiServices:

    def __init__(self):
        self.model_stt = WhisperModel("small", device="cpu", compute_type="int8")

    async def stt(self, file: UploadFile):
        # sauvegarde temporaire du fichier

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        segments, info = self.model_stt.transcribe(tmp_path, beam_size=5)

        result = " ".join(segment.text for segment in segments)

        return {"stt": result}