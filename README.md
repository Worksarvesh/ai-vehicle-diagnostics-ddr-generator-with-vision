# AI Vehicle Diagnostics

A production-ready vehicle diagnostic system built as a modular full-stack application.

This refactor converts the original research/demo project into a clean, deployable stack with:

- **FastAPI backend** for prediction and health checks
- **XGBoost model pipeline** with preprocessing, missing-value handling, and versioning
- **Simple responsive frontend** for live prediction input and confidence display
- **Analytics and logging** for prediction tracking
- **Docker-ready deployment**

## 🚀 Features

- `POST /predict` for structured diagnostic severity prediction
- `POST /predict-image` for optional image-augmented diagnostics
- `GET /health` for service health checks
- Image encoding via transfer learning with a pretrained ResNet18 backbone
- Validation with Pydantic and API-key authentication
- Model + preprocessing saved via `joblib`
- Training evaluation with precision, recall, F1-score, confusion matrix
- Responsive UI with instant feedback and probability distribution
- Structured logging and request analytics

## 📦 Repository Structure

- `/backend` - FastAPI service, schemas, auth, logging
- `/frontend` - static web UI for submitting inspection data
- `/ml_model` - training pipeline, model persistence, evaluation
- `/utils` - reusable helper utilities

## 🧪 Training the Model

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Train the model:

```bash
python ml_model/train.py
```

3. Confirm the model file is created at `ml_model/vehicle_diagnostics_xgb.pkl`.

## 🧑‍💻 Run the API Locally

1. Create a `.env` file from the example:

```bash
cp .env.example .env
```

2. Start the API:

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

3. Open the frontend in your browser:

- `frontend/index.html`

> If you serve the static HTML from a simple server, it can call the API at `http://localhost:8000`.

## 📡 API Endpoints

### `GET /health`

Returns service status and model metadata.

### `POST /predict`

Request body:

```json
{
  "engine_temp": 110.5,
  "brake_wear_pct": 30,
  "battery_voltage": 12.2,
  "tire_pressure": 31.0,
  "chain_tension": 50,
  "ambient_temp": 22.0,
  "smoke_detected": true,
  "abnormal_noise": false
}
```

### `POST /predict-image`

Accepts the same structured fields plus an optional image file upload as multipart form data. The backend extracts image features and improves diagnostics output.

Headers:

- `X-API-KEY: demo-key`

Response:

```json
{
  "model_version": "1.0.0",
  "predicted_severity": "medium",
  "confidence": 0.8432,
  "probabilities": {
    "high": 0.1123,
    "low": 0.1854,
    "medium": 0.7023
  },
  "message": "Vehicle diagnostic prediction completed successfully."
}
```

## 🧩 Frontend Usage

Open `frontend/index.html` in a browser and submit the inspection form.

- Uses the API to get prediction results
- Displays confidence and probability breakdown
- Supports error and loading states

## 🛠️ Deployment

Build and run with Docker:

```bash
docker compose up --build
```

Then open the frontend separately or deploy it behind a static file server.

## ✅ Notes

- The model is trained on a synthetic diagnostic dataset in `ml_model/data/vehicle_diagnostics.csv`.
- `backend/logs` stores API logs and prediction analytics.
- A basic API key is provided via `.env` / `.env.example`.

---

## Legacy

The original `/ai-ddr-generator` folder remains for reference but is no longer the main application path.
