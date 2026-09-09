from fastapi import APIRouter

from api.schemas import (
    Transaction,
    PredictionResponse,
)

from api.predictor import predict

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict_transaction(transaction: Transaction):

    result = predict(transaction.model_dump())

    return result