import json
import os
import threading
import time
from typing import Any, Dict, Optional

class JobStore:
    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            self._write({})

    # Read the json file
    def _read(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Write in the json file 
    def _write(self, data: Dict[str, Any]) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    # Create a new job in the json file
    def create(self, job_id: str, img_filename: str) -> Dict[str, Any]:
        now = time.time()
        job = {
            "id": job_id,
            "status": "queued",  # queued|running|done|failed|waiting_for_video
            "created_at": now,
            "updated_at": now,
            "img": img_filename,
            "reserved_video": None,
            "output_file": None,
            "frames": None,
            "swapped_frames": None,
            "error": None,
        }
        with self._lock:
            data = self._read()
            data[job_id] = job
            self._write(data)
        return job

    # get a job from job_id
    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._read().get(job_id)

    # Update a job data with **patch from job_id
    def update(self, job_id: str, **patch) -> Dict[str, Any]:
        now = time.time()
        with self._lock:
            data = self._read()
            job = data.get(job_id)
            if not job:
                raise KeyError(job_id)
            job.update(patch)
            job["updated_at"] = now
            data[job_id] = job
            self._write(data)
            return job
