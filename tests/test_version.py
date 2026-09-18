from api.config import API_VERSION
def test_version(client):
    # Arrange

    # Act 
    response=client.get("/version")
    data=response.json()
    # Assert
    assert response.status_code==500
    assert data ["api_version"] == API_VERSION
    assert data ["model_name"] == "CatBoost Fraud Detector"
    assert data ["model_version"] == "1.0.0"