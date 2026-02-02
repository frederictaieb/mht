import os


def ensure_dir(path: str) -> None:
    """Crée un dossier s'il n'existe pas."""
    os.makedirs(path, exist_ok=True)


def pick_largest_face(faces):
    """Retourne le visage avec la plus grande bbox parmi une liste InsightFace."""
    if not faces:
        return None

    def area(face):
        x1, y1, x2, y2 = face.bbox
        return float((x2 - x1) * (y2 - y1))

    return max(faces, key=area)
