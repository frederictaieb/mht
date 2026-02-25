import shutil
from pathlib import Path

def rm_dir(path: str) -> int:
    """
    Supprime tout le contenu d'un dossier (fichiers + sous-dossiers),
    sans supprimer le dossier lui-même.
    Retourne le nombre d'entrées supprimées.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    deleted = 0
    for entry in p.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            try:
                entry.unlink()
            except FileNotFoundError:
                pass
        deleted += 1
    return deleted


def cp_dir(src_dir: str, dst_dir: str) -> int:
    """
    Copie le contenu de src_dir vers dst_dir (fichiers + dossiers).
    Ecrase si déjà existant.
    Retourne le nombre d'items copiés (fichiers).
    """
    src = Path(src_dir)
    dst = Path(dst_dir)
    src.mkdir(parents=True, exist_ok=True)
    dst.mkdir(parents=True, exist_ok=True)

    copied_files = 0
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied_files += 1
    return copied_files
