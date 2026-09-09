from fastapi import APIRouter
from api.config import (
    API_VERSION,
    MODEL_NAME,
    MODEL_VERSION,
     MODEL_TYPE,
    ALGORITHM,
)
from api.schemas import VersionInfo,ModelInfo
from api.predictor import threshold

router = APIRouter()


@router.get("/version",response_model=VersionInfo)
def version():

    return {

        "api_version": API_VERSION,

        "model_name": MODEL_NAME,

        "model_version": MODEL_VERSION

    }

@router.get(
    "/model",
    response_model=ModelInfo
)
def model_info():

    return {

        "model_name": MODEL_NAME,

        "algorithm": ALGORITHM,

        "model_type": MODEL_TYPE,

        "model_version": MODEL_VERSION,

        "threshold": threshold,
    }