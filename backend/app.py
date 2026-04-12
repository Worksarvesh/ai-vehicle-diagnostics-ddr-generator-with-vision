from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.auth import api_key_auth
from backend.image_inspector import extract_image_features
from backend.logging_config import logger
from backend.model_loader import ModelService
from backend.schemas import PredictionRequest, PredictionResponse

load_dotenv()

app = FastAPI(
    title="AI Vehicle Diagnostics",
    description="Production-ready REST API for vehicle diagnostic predictions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_service = ModelService()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"detail": "Server error occurred. Please check logs for details."},
    )


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_version": model_service.model_version,
        "model_path": str(model_service.model_path),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, x_api_key: str = Header(..., alias="X-API-KEY")):
    if not api_key_auth(x_api_key):
        logger.warning("Unauthorized prediction attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")

    payload = request.dict()
    logger.info("Received prediction request", extra={"payload": payload})

    try:
        prediction = model_service.predict(payload)
        logger.info("Prediction complete", extra={"prediction": prediction})
        return prediction
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed. See logs for details.")


@app.post("/predict-image", response_model=PredictionResponse)
async def predict_image(
    engine_temp: float = Form(...),
    brake_wear_pct: float = Form(...),
    battery_voltage: float = Form(...),
    tire_pressure: float = Form(...),
    chain_tension: float = Form(...),
    ambient_temp: float = Form(...),
    smoke_detected: bool = Form(...),
    abnormal_noise: bool = Form(...),
    x_api_key: str = Header(..., alias="X-API-KEY"),
    image: UploadFile | None = File(None),
):
    if not api_key_auth(x_api_key):
        logger.warning("Unauthorized image prediction attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")

    payload = {
        "engine_temp": engine_temp,
        "brake_wear_pct": brake_wear_pct,
        "battery_voltage": battery_voltage,
        "tire_pressure": tire_pressure,
        "chain_tension": chain_tension,
        "ambient_temp": ambient_temp,
        "smoke_detected": smoke_detected,
        "abnormal_noise": abnormal_noise,
    }

    image_features = {}
    if image is not None:
        logger.info("Image uploaded for prediction", extra={"image_name": image.filename})
        image_bytes = await image.read()
        image_features = extract_image_features(image_bytes)
        payload.update(image_features)

    logger.info("Received prediction request with image", extra={"payload": payload})

    try:
        prediction = model_service.predict(payload)
        prediction["image_features"] = image_features or None
        logger.info("Image prediction complete", extra={"prediction": prediction})
        return prediction
    except Exception as exc:
        logger.exception("Image prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed. See logs for details.")
