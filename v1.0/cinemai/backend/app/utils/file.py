import re

def clean_name(self, value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^a-z0-9_-]", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")