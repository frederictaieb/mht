import json
import torch
import numpy as np
from qwen_tts import VoiceClonePromptItem

def serialize_voice_clone_prompt_item(item):
    if hasattr(item, "model_dump"):
        data = item.model_dump()
    else:
        data = vars(item)
    result = {}

    for k, v in data.items():
        if isinstance(v, torch.Tensor):
            result[k] = v.cpu().tolist()
        elif isinstance(v, np.ndarray):
            result[k] = v.tolist()
        else:
            result[k] = v
    return result

def deserialize_voice_clone_prompt(prompt_json: str) -> list[VoiceClonePromptItem]:
    """
    Reconstruit une liste de VoiceClonePromptItem à partir du JSON stocké en base.
    """
    data = json.loads(prompt_json)
    result = []
    for item in data:
        reconstructed = {}
        for k, v in item.items():
            # liste → tensor (cas fréquent pour embeddings)
            if isinstance(v, list):
                try:
                    reconstructed[k] = torch.tensor(v)
                except Exception:
                    reconstructed[k] = v
            else:
                reconstructed[k] = v
        result.append(VoiceClonePromptItem(**reconstructed))
    return result