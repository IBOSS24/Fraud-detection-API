from api.config import DEFAULT_THRESHOLD
def test_model(client):
    # Arrange

    # Act 
    response=client.get("/model")
    data = response.json()

    # Assert
    assert response.status_code==200
    assert data ["model_name"] == "CatBoost Fraud Detector"
    assert data ["algorithm"] == "CatBoostClassifier"
    assert data ["model_type"] == "Binary Classification"
    assert data ["model_version"] == "1.0.0"
    
    assert isinstance(data["threshold"], float) 
    assert 0 < data["threshold"] < 1
    assert data["threshold"] == DEFAULT_THRESHOLD

