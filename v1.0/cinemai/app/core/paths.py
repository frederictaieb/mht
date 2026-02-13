import os
from fastapi import HTTPException

def resolve_under(base_dir: str, user_path: str) -> str:
    base_dir = os.path.abspath(base_dir)

    candidate = user_path
    if not os.path.isabs(candidate):
        candidate = os.path.join(base_dir, candidate)
    candidate = os.path.abspath(candidate)

    if os.path.commonpath([base_dir, candidate]) != base_dir:
        raise HTTPException(status_code=400, detail=f"Chemin interdit: {user_path}")
    return candidate
