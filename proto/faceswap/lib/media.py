import subprocess
from typing import Sequence


def run(cmd: Sequence[str]) -> tuple[int, str, str]:
    """Exécute une commande et renvoie (returncode, stdout, stderr)."""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr


def ffmpeg_exists() -> bool:
    """Retourne True si ffmpeg est disponible."""
    return run(["ffmpeg", "-version"])[0] == 0


def extract_audio(in_video: str, out_audio: str) -> tuple[int, str, str]:
    """Extrait l'audio d'une vidéo (copie du flux audio si possible)."""
    return run(["ffmpeg", "-y", "-i", in_video, "-vn", "-acodec", "copy", out_audio])


def mux_audio(video_no_audio: str, audio_file: str, out_video: str) -> tuple[int, str, str]:
    """Remux audio + vidéo. Vidéo copiée, audio ré-encodé en AAC."""
    return run([
        "ffmpeg", "-y",
        "-i", video_no_audio,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        out_video
    ])
