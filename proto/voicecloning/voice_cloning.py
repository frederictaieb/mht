import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

TEXT = """
Parle uniquement en français, avec une voix naturelle.

Bonjour Frédéric. [chuckle]
Je vais maintenant parler en français.
Je suis content de te retrouver. [laugh]
Ensuite je redeviens sérieux. Nous allons tester une intonation plus posée.
"""

REF = "ref.wav"
OUT = "out_fr.wav"


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)

    print("Loading model...")
    model = ChatterboxTTS.from_pretrained(device=device)

    print("Generating...")
    wav = model.generate(
        TEXT.strip(),
        audio_prompt_path=REF,
        exaggeration=0.8,
        cfg=0.4,
        temperature=0.7,
    )

    ta.save(OUT, wav, model.sr)
    print("✅ Généré:", OUT)


if __name__ == "__main__":
    main()
