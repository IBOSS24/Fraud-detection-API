def test_version(client):
    # Arrange

    # Act 
    response=client.get("/version")
    data=response.json()
    # Assert
    assert response.status_code==200
    assert data ["api_version"] == "1.0.0"
    assert data ["model_name"] == "CatBoost Fraud Detector"
    assert data ["model_version"] == "1.0.0"