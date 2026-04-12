from pydantic import BaseModel, Field
from typing import Dict, Optional


class PredictionRequest(BaseModel):
    engine_temp: float = Field(..., ge=0, le=250, description="Engine temperature in Celsius")
    brake_wear_pct: float = Field(..., ge=0, le=100, description="Brake pad wear percentage")
    battery_voltage: float = Field(..., ge=0, le=30, description="Battery voltage in volts")
    tire_pressure: float = Field(..., ge=0, le=60, description="Average tire pressure in PSI")
    chain_tension: float = Field(..., ge=0, le=100, description="Chain tension score")
    ambient_temp: float = Field(..., ge=-40, le=80, description="Ambient temperature in Celsius")
    smoke_detected: bool = Field(..., description="Whether smoke was detected during inspection")
    abnormal_noise: bool = Field(..., description="Whether abnormal noise was detected during inspection")


class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    model_version: str
    predicted_severity: str
    confidence: float
    probabilities: Dict[str, float]
    image_features: Optional[Dict[str, float]] = None
    message: str
