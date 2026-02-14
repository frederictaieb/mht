import os
import insightface
from insightface.app import FaceAnalysis
from fastapi import HTTPException

class InsightFaceRuntime:
    def __init__(self, model_path: str, ctx_id: int, det_size=(640, 640), providers=None):
        self.model_path = model_path
        self.ctx_id = ctx_id
        self.det_size = det_size
        self.providers = providers or ["CPUExecutionProvider"]

        self.app_face = None
        self.swapper = None

    def load(self):
        if not os.path.exists(self.model_path):
            raise HTTPException(status_code=500, detail=f"Modèle swapper introuvable: {self.model_path}")

        self.app_face = FaceAnalysis(name="buffalo_l")
        self.app_face.prepare(ctx_id=self.ctx_id, det_size=self.det_size)

        self.swapper = insightface.model_zoo.get_model(
            self.model_path,
            providers=self.providers
        )

    def ensure_loaded(self):
        if self.app_face is None or self.swapper is None:
            self.load()

