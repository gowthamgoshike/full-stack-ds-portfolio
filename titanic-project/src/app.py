from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Titanic Survival Predictor")

# Input Schema
class Passenger(BaseModel):
    Pclass: int
    SibSp: int
    Parch: int
    Age: float

# Load Model
model_path = 'models/decision_tree.pkl'
model = joblib.load(model_path) if os.path.exists(model_path) else None

@app.get("/")
def home():
    return {"status": "online", "message": "Titanic API Ready 🚢"}

@app.post("/predict")
def predict(p: Passenger):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Convert to DataFrame
    data = pd.DataFrame([p.dict()])
    
    # Predict
    prediction = int(model.predict(data)[0])
    label = "Survived" if prediction == 1 else "Died"
    
    return {"survived": prediction, "label": label}