# backend/app/services/insightface_runtime.py
import os
import platform
import insightface
import onnxruntime as ort
from insightface.app import FaceAnalysis
from fastapi import HTTPException


def choose_ort_providers() -> list[str]:
    available = ort.get_available_providers()

    gpu_priority = [
        "TensorrtExecutionProvider",
        "CUDAExecutionProvider",
        "ROCMExecutionProvider",
        "DmlExecutionProvider",
        "OpenVINOExecutionProvider",
    ]
    chosen = [p for p in gpu_priority if p in available]
    if chosen:
        if "CPUExecutionProvider" in available and "CPUExecutionProvider" not in chosen:
            chosen.append("CPUExecutionProvider")
        return chosen

    if platform.system().lower() == "darwin" and "CoreMLExecutionProvider" in available:
        return ["CoreMLExecutionProvider", "CPUExecutionProvider"]

    return ["CPUExecutionProvider"]


def choose_ctx_id(providers: list[str]) -> int:
    gpu_like = {
        "TensorrtExecutionProvider",
        "CUDAExecutionProvider",
        "ROCMExecutionProvider",
        "DmlExecutionProvider",
        "OpenVINOExecutionProvider",
    }
    return 0 if any(p in gpu_like for p in providers) else -1


class InsightFaceRuntime:
    def __init__(
        self,
        model_path: str,
        ctx_id: int | None = None,          # <- re-accept ctx_id
        det_size=(640, 640),
        providers: list[str] | None = None,
    ):
        self.model_path = model_path
        self.det_size = det_size

        self.providers = providers or choose_ort_providers()
        self.ctx_id = ctx_id if ctx_id is not None else choose_ctx_id(self.providers)

        self.app_face = None
        self.swapper = None

    def load(self):
        if not os.path.exists(self.model_path):
            raise HTTPException(status_code=500, detail=f"Modèle swapper introuvable: {self.model_path}")

        print("system:", platform.system())
        print("ort available:", ort.get_available_providers())
        print("requested providers:", self.providers)

        # IMPORTANT: providers ici aussi
        self.app_face = FaceAnalysis(name="buffalo_l", providers=self.providers)
        self.app_face.prepare(ctx_id=self.ctx_id, det_size=self.det_size)

        self.swapper = insightface.model_zoo.get_model(self.model_path, providers=self.providers)

    def ensure_loaded(self):
        if self.app_face is None or self.swapper is None:
            self.load()