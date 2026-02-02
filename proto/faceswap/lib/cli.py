import argparse


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()

    # Mode single
    ap.add_argument("--source", help="Image source (visage à copier)")
    ap.add_argument("--video", help="Vidéo cible à modifier")
    ap.add_argument("--out", help="Vidéo de sortie (mode single)")

    # Mode batch
    ap.add_argument("--json", default="batch.json", help="Fichier JSON batch")
    ap.add_argument("--input-dir", default="input", help="Répertoire d'entrée")
    ap.add_argument("--output-dir", default="output", help="Répertoire de sortie")

    # Options
    ap.add_argument("--swapper", default="./models/inswapper_128.onnx", help="Chemin inswapper_128.onnx")
    ap.add_argument("--det-size", default="640,640", help="Taille détection ex: 640,640")
    ap.add_argument("--max-width", type=int, default=0, help="Resize si width > max-width (0=off)")
    ap.add_argument("--every", type=int, default=1, help="Traite 1 frame sur N (1=toutes)")
    ap.add_argument("--keep-audio", action="store_true", help="Conserver l'audio si ffmpeg dispo")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "coreml"])

    return ap
