from api.predictor import MODEL_LOADED
from unittest.mock import  patch
from api.config import API_VERSION
def test_health_model_is_loaded(client):
    # Arrange
    with patch("api.routers.health.MODEL_LOADED", True):
        # Act
        response = client.get("/health")
        data = response.json()
        # Assert
        assert response.status_code == 200
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        assert data["api_version"] == API_VERSION
        assert data["model_version"] == "1.0.0"


def test_health_model_not_loaded(client):
    # Arrange
    with patch("api.routers.health.MODEL_LOADED", False):
        # Act
        response = client.get("/health")
        data = response.json()
        # Assert
        assert response.status_code == 503
        assert data["status"] == "unhealthy"
        assert data["model_loaded"] is False
        assert data["api_version"] == API_VERSION
        assert data["model_version"] == "1.0.0"
