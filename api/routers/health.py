from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.config import API_VERSION, MODEL_VERSION
from api.predictor import MODEL_LOADED

router = APIRouter()


@router.get("/health")
def health_check():
    if MODEL_LOADED:
        return {
            "status": "healthy",
            "model_loaded": True,
            "api_version": API_VERSION,
            "model_version": MODEL_VERSION,
        }

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "unhealthy",
            "model_loaded": False,
            "api_version": API_VERSION,
            "model_version": MODEL_VERSION,
        },
    )