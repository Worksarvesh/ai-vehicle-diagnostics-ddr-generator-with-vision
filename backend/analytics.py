import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "predictions.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_prediction(payload: dict, prediction: dict) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload,
        "prediction": prediction,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
