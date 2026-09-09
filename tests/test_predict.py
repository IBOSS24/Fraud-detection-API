from api.config import DEFAULT_THRESHOLD
from unittest.mock import  patch


def test_predict_fraud_transaction(client, fraud_transaction):
    # Arrange
    
    
    # Act
    response = client.post("/predict", json=fraud_transaction)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert isinstance(data["prediction_label"], int)
    assert data["prediction_label"]==1 
    assert isinstance(data["fraud_probability"], float)
    assert data["fraud_probability"] >= DEFAULT_THRESHOLD

def test_predict_legitimate_transaction(client, legitimate_transaction):
    # Arrange
    
    # Act
    response = client.post("/predict", json=legitimate_transaction)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert isinstance(data["prediction_label"], int)
    assert data["prediction_label"]==0 
    assert isinstance(data["fraud_probability"], float)
    assert data["fraud_probability"] < DEFAULT_THRESHOLD

def test_predict_missing_amount(client, fraud_transaction):
    # Arrange
    payload = fraud_transaction.copy()
    payload.pop("Amount", None)
    # Act
    response = client.post("/predict", json=payload)
    data = response.json()
    # Assert
    assert response.status_code == 422


@patch("api.predictor.model")
def test_predict_fraud_mock(mock_model, client,fraud_transaction):
    # Arrange
    mock_model.predict_proba.return_value = [[0.05, 0.95]]
    # Act
    response = client.post("/predict", json=fraud_transaction)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data["prediction_label"] == 1
    assert data["fraud_probability"] == 0.95
    mock_model.predict_proba.assert_called_once()

@patch("api.predictor.model")
def test_predict_crash(mock_model, client,fraud_transaction):
    # Arrange
    mock_model.predict_proba.side_effect = RuntimeError(
        "Model crashed"
     )
    # Act
    response = client.post("/predict", json=fraud_transaction)
    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == "Prediction failed"
