#api/predictor.py
from fastapi import HTTPException
import json
from pathlib import Path

import pandas as pd
from pycaret.classification import load_model

from api.config import (
    MODEL_PATH,
    MODEL_VERSION, 
    THRESHOLD_PATH,
    DEFAULT_THRESHOLD ,
)
from api.utils import setup_logger

logger = setup_logger()

MODEL_FILE = Path(f"{MODEL_PATH}.pkl")

logger.info(f"Loading model from: {MODEL_FILE}")

if not MODEL_FILE.exists():
    logger.error(f"Model file not found: {MODEL_FILE}")
    raise FileNotFoundError(
        f"Model file not found: {MODEL_FILE}"
    )

model = load_model(MODEL_PATH)

logger.info(
    f"Model '{MODEL_VERSION}' loaded successfully "
    f"from '{MODEL_FILE.name}'."
)
MODEL_LOADED = model is not None

try:
    with open(THRESHOLD_PATH, "r") as file:
        threshold = json.load(file)["threshold"]
        logger.info(f"Using prediction threshold: {threshold}")

except (FileNotFoundError, json.JSONDecodeError, KeyError):
    logger.warning(
        f"Could not load threshold from '{THRESHOLD_PATH}'. "
        f"Using default threshold: {DEFAULT_THRESHOLD}"
    )
    threshold = DEFAULT_THRESHOLD
    
# Validate the threshold that will actually be used
if not 0 <= threshold <= 1:
    logger.error(f"Invalid threshold: {threshold}")
    raise ValueError("Threshold must be between 0 and 1.")

def predict(transaction: dict)->dict:
    """
    Predict whether a transaction is fraudulent.

    Args:
        transaction: Dictionary containing transaction features.

    Returns:
        Dictionary with prediction result and probability.
    """    
    try:
        input_data = pd.DataFrame([transaction])

        # logger.info("\n%s", prediction.to_string())

        class_probabilities = model.predict_proba(input_data)[0]
        # Probability of the positive (fraud) class
        POSITIVE_CLASS = 1
        fraud_probability = float(class_probabilities[POSITIVE_CLASS])
        label = int(fraud_probability >= threshold)
    
        # Log successful prediction
        prediction = "Fraud" if label == 1 else "Legitimate"

        logger.info(
                f"Prediction completed | "
                f"Prediction={prediction} | "
                f"Fraud Probability={fraud_probability:.6f} | "
                f"Threshold={threshold}"
                )
        return {
            "prediction_label": label,
            "fraud_probability": round(fraud_probability, 4),
            "threshold": threshold,
            "model_version": MODEL_VERSION,
        }
        
    except Exception :
        logger.exception(
            "Prediction failed while processing the transaction."
        )
        raise HTTPException(
        status_code=500,
        detail="Prediction failed"
        )
