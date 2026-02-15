import os
from pathlib import Path
from typing import Optional, Tuple

def _numeric_key(p: Path) -> Tuple[int, str]:
    try:
        return (int(p.stem), p.name)
    except ValueError:
        return (10**9, p.name)

class VideoPool:
    def __init__(self, base_vid_dir: str):
        self.base = Path(base_vid_dir)
        self.available = self.base / "available"
        self.in_progress = self.base / "in_progress"
        self.used = self.base / "used"

        self.available.mkdir(parents=True, exist_ok=True)
        self.in_progress.mkdir(parents=True, exist_ok=True)
        self.used.mkdir(parents=True, exist_ok=True)

    # From available to in_progress
    def reserve_next(self, job_id: str) -> Optional[str]:
        # Create list of video in the folder available
        vids = [p for p in self.available.iterdir() if p.is_file()]
        # Sort the list
        vids.sort(key=_numeric_key)
        # If no video, return
        if not vids:
            return None
        # Take the first video
        src = vids[0]
        # New name with job id
        reserved_name = f"{job_id}-{src.name}"
        # path in in_progress folder
        dst = self.in_progress / reserved_name
        # move the video to in_progress folder withnew name
        os.replace(str(src), str(dst))  # move atomique
        # return new names
        return reserved_name

    # From in_progress to used
    def mark_used(self, reserved_name: str) -> None:
        # create path of the in_progress video
        src = self.in_progress / reserved_name
        # create path of the used video
        dst = self.used / reserved_name
        # move the video from in_progress folder to used folder
        if src.exists():
            os.replace(str(src), str(dst))

    # Reverse action in case of error : from in_progress to available 
    def release_back(self, reserved_name: str) -> None:
        # create path of the in_progress video
        src = self.in_progress / reserved_name
        # remove the job id from the filename to have the original name of the video
        original = reserved_name.split("-", 1)[1] if "-" in reserved_name else reserved_name
        # create path of the original available video
        dst = self.available / original
        # move the video from in_progress folder to available folder 
        if src.exists():
            os.replace(str(src), str(dst))
