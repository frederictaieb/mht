from __future__ import annotations

from insightface.app import FaceAnalysis
import insightface


def available_ort_providers(logger=None) -> list[str]:
    """Liste les providers onnxruntime disponibles."""
    try:
        import onnxruntime as ort
        return ort.get_available_providers()
    except Exception as e:
        if logger:
            logger.warning(f"onnxruntime non importable -> CPU only ({e})")
        return []


def pick_execution_providers(device: str, logger=None) -> tuple[list[str], bool]:
    """
    device: auto|cpu|cuda|coreml
    Retourne (providers, use_gpu)
    """
    providers = available_ort_providers(logger)

    if device == "cpu":
        return ["CPUExecutionProvider"], False

    if device == "cuda":
        if "CUDAExecutionProvider" in providers:
            return ["CUDAExecutionProvider", "CPUExecutionProvider"], True
        if logger:
            logger.warning("CUDA demandé mais indisponible -> CPU")
        return ["CPUExecutionProvider"], False

    if device == "coreml":
        if "CoreMLExecutionProvider" in providers:
            return ["CoreMLExecutionProvider", "CPUExecutionProvider"], True
        if logger:
            logger.warning("CoreML demandé mais indisponible -> CPU")
        return ["CPUExecutionProvider"], False

    # auto
    preferred: list[str] = []
    if "CUDAExecutionProvider" in providers:
        preferred.append("CUDAExecutionProvider")
    if "CoreMLExecutionProvider" in providers:
        preferred.append("CoreMLExecutionProvider")
    preferred.append("CPUExecutionProvider")

    use_gpu = any(p in ("CUDAExecutionProvider", "CoreMLExecutionProvider") for p in preferred)
    return preferred, use_gpu


def init_models(
    *,
    swapper_path: str,
    det_size: tuple[int, int],
    device: str,
    logger=None,
):
    """
    Initialise FaceAnalysis + modèle swapper.
    Retourne (app, swapper, providers, use_gpu)
    """
    providers, use_gpu = pick_execution_providers(device, logger)

    app = FaceAnalysis(name="buffalo_l")
    # ctx_id: 0 uniquement quand CUDA est réellement utilisé côté insightface
    app.prepare(ctx_id=0 if "CUDAExecutionProvider" in providers else -1, det_size=det_size)

    swapper = insightface.model_zoo.get_model(swapper_path, providers=providers)

    return app, swapper, providers, use_gpu
