import pytest
import pandas as pd
import os
from fastapi.testclient import TestClient
from src.app import app
from src.features.validate import validate_schema

# 1. Test Data Validation
def test_validation_catches_missing_columns():
    bad_df = pd.DataFrame({'Age': [20]}) # Missing Pclass, etc.
    with pytest.raises(ValueError):
        validate_schema(bad_df)

# 2. Test API Safety
client = TestClient(app)

def test_api_health():
    response = client.get("/")
    assert response.status_code == 200

def test_api_rejects_bad_types():
    # Sending "Age" as a string instead of number
    bad_payload = {"Pclass": 1, "SibSp": 0, "Parch": 0, "Age": "Old"}
    response = client.post("/predict", json=bad_payload)
    assert response.status_code == 422 # Validation Error