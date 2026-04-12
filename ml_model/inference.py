import sys
from pathlib import Path
from typing import Dict, Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import joblib

MODEL_PATH = ROOT_DIR / "ml_model" / "vehicle_diagnostics_xgb.pkl"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. Run ml_model/train.py first."
        )
    return joblib.load(MODEL_PATH)


def predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = load_model()
    features = pd.DataFrame([payload])
    labels = (
        pipeline.label_encoder.classes_
        if hasattr(pipeline, "label_encoder")
        else pipeline.named_steps["classifier"].classes_
    )
    probabilities = pipeline.predict_proba(features)[0]
    encoded_prediction = pipeline.predict(features)[0]
    predicted_severity = (
        pipeline.label_encoder.inverse_transform([encoded_prediction])[0]
        if hasattr(pipeline, "label_encoder")
        else str(encoded_prediction)
    )
    return {
        "predicted_severity": predicted_severity,
        "confidence": round(float(max(probabilities)), 4),
        "probabilities": {label: round(float(score), 4) for label, score in zip(labels, probabilities)},
    }
