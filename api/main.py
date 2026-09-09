from fastapi import FastAPI

from api.config import API_TITLE, API_VERSION
from api.routers.health import router as health_router
from api.routers.prediction import router as prediction_router
from api.routers.info import router as info_router

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
)


@app.get("/")
def home():
    return {
        "message": "Fraud Detection API is running."
    }


app.include_router(health_router)
app.include_router(info_router)
app.include_router(prediction_router)
