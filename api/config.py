# api/config.py

from pathlib import Path

# ----------------------------
# Project Directories
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# ----------------------------
# Files
# ----------------------------

MODEL_PATH = MODELS_DIR / "fraud_detector"
THRESHOLD_PATH = MODELS_DIR / "threshold.json"
LOG_FILE = LOGS_DIR / "app.log"

# ----------------------------
# API Settings
# ----------------------------

API_TITLE = "Fraud Detection API"
API_VERSION = "1.1.2"

# ----------------------------
# Model Settings
# ----------------------------
MODEL_NAME = "CatBoost Fraud Detector"
MODEL_VERSION = "1.0.0"
MODEL_TYPE = "Binary Classification"
ALGORITHM = "CatBoostClassifier"

# ----------------------------
# Default Prediction Threshold
# ----------------------------

DEFAULT_THRESHOLD = 0.50

