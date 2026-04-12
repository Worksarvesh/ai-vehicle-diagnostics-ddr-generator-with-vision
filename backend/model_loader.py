import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Any

DEFAULT_IMAGE_FEATURES = {
    "image_brightness": 0.0,
    "image_contrast": 0.0,
    "image_edge_density": 0.0,
    "image_dark_ratio": 0.0,
    "image_red_ratio": 0.0,
    "image_green_ratio": 0.0,
    "image_blue_ratio": 0.0,
    "image_embedding_mean": 0.0,
    "image_embedding_std": 0.0,
    "image_embedding_max": 0.0,
    "image_embedding_l2": 0.0,
}


class ModelService:
    def __init__(self) -> None:
        self.model_path = Path(__file__).resolve().parents[1] / "ml_model" / "vehicle_diagnostics_xgb.pkl"
        self.model_version = "1.0.0"
        self.pipeline = self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Trained model not found at {self.model_path}. Run ml_model/train.py first."
            )
        return joblib.load(self.model_path)

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        for key, default_value in DEFAULT_IMAGE_FEATURES.items():
            payload.setdefault(key, default_value)

        features = pd.DataFrame([payload])
        probabilities = self.pipeline.predict_proba(features)[0]
        encoded_prediction = self.pipeline.predict(features)[0]
        prediction_label = (
            self.pipeline.label_encoder.inverse_transform([encoded_prediction])[0]
            if hasattr(self.pipeline, "label_encoder")
            else str(encoded_prediction)
        )

        labels = (
            self.pipeline.label_encoder.classes_
            if hasattr(self.pipeline, "label_encoder")
            else self.pipeline.named_steps["classifier"].classes_
        )

        result = {
            "model_version": self.model_version,
            "predicted_severity": prediction_label,
            "confidence": round(float(max(probabilities)), 4),
            "probabilities": {
                label: round(float(prob), 4) for label, prob in zip(labels, probabilities)
            },
            "message": "Vehicle diagnostic prediction completed successfully.",
        }
        return result
