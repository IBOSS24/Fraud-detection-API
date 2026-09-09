# api/schemas.py
from pydantic import BaseModel,Field


class Transaction(BaseModel):
    Time: float = Field(
        ge=0,
        description="Elapsed time since the first transaction."
    )

    Amount: float = Field(
        ge=0,
        description="Transaction amount in dollars."
    )
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float



class PredictionResponse(BaseModel):
    prediction_label: int
    fraud_probability: float
    threshold: float
    model_version: str

class VersionInfo(BaseModel):
    api_version: str
    model_name: str
    model_version: str

class ModelInfo(BaseModel):

    model_name: str

    algorithm: str

    model_type: str

    model_version: str

    threshold: float
# swagger knows what goes into the API and what comes out the API