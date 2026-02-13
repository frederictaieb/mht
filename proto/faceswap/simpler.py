import os
import subprocess
import tempfile

import cv2
import insightface
from insightface.app import FaceAnalysis


def pick_largest_face(faces):
    if not faces:
        return None

    def area(face):
        x1, y1, x2, y2 = face.bbox
        return float((x2 - x1) * (y2 - y1))

    return max(faces, key=area)


def ffmpeg_exists():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except Exception:
        return False


def extract_audio(in_video, out_audio):
    # Copie l’audio tel quel (si possible)
    p = subprocess.run(
        ["ffmpeg", "-y", "-i", in_video, "-vn", "-acodec", "copy", out_audio],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p.returncode == 0


def mux_audio(video_no_audio, audio_file, out_video):
    # Recolle l’audio (ré-encode en AAC pour compatibilité)
    p = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_no_audio,
            "-i",
            audio_file,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            out_video,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p.returncode == 0


def ensure_parent_dir(path: str):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def main():
    # --- Paths (modifie ici si besoin) ---
    source_image_path = "./input/1.jpg"
    input_video_path = "./input/1.mp4"
    output_video_path = "./output/1.mp4"
    swapper_model_path = "./models/inswapper_128.onnx"

    keep_audio = True  # mets à False si tu veux ignorer l'audio

    ensure_parent_dir(output_video_path)

    # --- Init InsightFace ---
    app = FaceAnalysis(name="buffalo_l")
    # ctx_id=-1 => CPU ; mets 0 si tu as CUDA correctement installé
    app.prepare(ctx_id=-1, det_size=(640, 640))

    # --- Load swapper model ---
    if not os.path.exists(swapper_model_path):
        raise FileNotFoundError(f"Modèle swapper introuvable: {swapper_model_path}")

    # Providers: CPU par défaut (plus robuste)
    swapper = insightface.model_zoo.get_model(
        swapper_model_path,
        providers=["CPUExecutionProvider"],
    )

    # --- Load source image ---
    src_img = cv2.imread(source_image_path)
    if src_img is None:
        raise ValueError(f"Impossible de lire l'image source: {source_image_path}")

    # --- Detect source face ---
    src_faces = app.get(src_img)
    src_face = pick_largest_face(src_faces)
    if src_face is None:
        raise RuntimeError("Aucun visage détecté dans l'image source.")

    # --- Open video ---
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la vidéo: {input_video_path}")

    # --- Video properties ---
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # --- Temp workspace ---
    tmp_dir = tempfile.mkdtemp(prefix="faceswap_")
    tmp_video = os.path.join(tmp_dir, "video_no_audio.mp4")

    # --- Video writer ---
    # mp4v marche souvent, sinon essaye avc1 ou écris en .avi + ffmpeg
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp_video, fourcc, fps, (w, h))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Impossible d'initialiser le writer vidéo (mp4v).")

    print("Processing frames...")
    frame_idx = 0
    swapped_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        # Détecter visage cible (plus grand) et swap si trouvé
        tgt_faces = app.get(frame)
        tgt_face = pick_largest_face(tgt_faces)

        if tgt_face is not None:
            # swapper.get(img, target_face, source_face, paste_back=True)
            frame = swapper.get(frame, tgt_face, src_face, paste_back=True)
            swapped_frames += 1

        writer.write(frame)

        if frame_idx % 60 == 0:
            print(f"{frame_idx} frames... (swapped: {swapped_frames})")

    cap.release()
    writer.release()

    # --- Audio (optionnel) ---
    if keep_audio and ffmpeg_exists():
        tmp_audio = os.path.join(tmp_dir, "audio_track")
        # Essaye d’extraire en "copy" (format dépend de la source)
        # On ne force pas l'extension pour éviter certains soucis
        extracted = extract_audio(input_video_path, tmp_audio)
        if extracted:
            # Mux en réencodant AAC
            tmp_final = os.path.join(tmp_dir, "final_with_audio.mp4")
            if mux_audio(tmp_video, tmp_audio, tmp_final):
                os.replace(tmp_final, output_video_path)
                print(f"OK (avec audio) -> {output_video_path}")
                return

        print("Audio: échec -> sortie sans audio.")

    # --- Fallback sans audio ---
    os.replace(tmp_video, output_video_path)
    print(f"OK -> {output_video_path}")


if __name__ == "__main__":
    main()
