from typing import Any
import json
import os

def save_json(data: Any, filepath: str) -> None:
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(filepath: str) -> Any:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    with open(filepath, 'r') as f:
        return json.load(f)

def save_model(model: Any, filepath: str) -> None:
    import joblib
    joblib.dump(model, filepath)

def load_model(filepath: str) -> Any:
    import joblib
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The model file {filepath} does not exist.")
    return joblib.load(filepath)