import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from ml_model.pipeline import build_pipeline, NUMERIC_FEATURES, CATEGORICAL_FEATURES

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "ml_model" / "data" / "vehicle_diagnostics.csv"
MODEL_PATH = ROOT_DIR / "ml_model" / "vehicle_diagnostics_xgb.pkl"
REPORT_PATH = ROOT_DIR / "ml_model" / "model_report.txt"


def load_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset missing at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=["id"], errors="ignore")
    return df


def prepare_data(df: pd.DataFrame):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df["issue_severity"]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def save_model(pipeline):
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved trained model to {MODEL_PATH}")


def write_report(report: str):
    with open(REPORT_PATH, "w", encoding="utf-8") as output_file:
        output_file.write(report)
    print(f"Saved model evaluation report to {REPORT_PATH}")


def run_training():
    df = load_dataset()
    X_train, X_test, y_train, y_test = prepare_data(df)

    encoder = LabelEncoder().fit(y_train)
    y_train_encoded = encoder.transform(y_train)
    y_test_encoded = encoder.transform(y_test)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train_encoded)
    pipeline.label_encoder = encoder

    y_pred_encoded = pipeline.predict(X_test)
    y_pred = encoder.inverse_transform(y_pred_encoded)

    report = classification_report(y_test, y_pred, digits=4)
    matrix = confusion_matrix(y_test, y_pred, labels=encoder.classes_)

    metrics_text = (
        "MODEL EVALUATION REPORT\n"
        "=======================\n\n"
        f"Classification Report:\n{report}\n"
        f"Confusion Matrix (rows=true labels, columns=predicted labels):\n{matrix}\n"
    )

    save_model(pipeline)
    write_report(metrics_text)
    print("Training complete.")


if __name__ == "__main__":
    run_training()
