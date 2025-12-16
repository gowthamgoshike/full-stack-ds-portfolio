from fastapi import FastAPI, HTTPException
from analytics_pkg.science import DataScienceEngine
import pandas as pd

app = FastAPI(title="Retail Intelligence API")
engine = DataScienceEngine()

@app.get("/")
def health_check():
    return {"status": "online", "message": "Enterprise AI Ready"}

@app.get("/analysis/outliers")
def get_outliers():
    """Returns outliers via IQR Method"""
    df = engine.get_clean_data()
    df_processed, lower, upper = engine.detect_outliers(df, 'amount')
    
    # Filter for API response (JSON friendly)
    outliers = df_processed[df_processed['is_outlier'] == True]
    
    # Replace Infinity/NaN values for JSON safety
    outliers = outliers.fillna(0)
    
    return {
        "lower_fence": float(lower),
        "upper_fence": float(upper),
        "outlier_count": int(len(outliers)),
        "data": outliers.to_dict(orient="records")
    }

@app.get("/prediction/return-risk")
def predict_risk(category: str):
    """Calculates Bayes Risk for a category"""
    try:
        prob = engine.calculate_bayes_return_prob(category)
        return {
            "category": category,
            "return_probability": float(prob),
            "risk_verdict": "High Risk" if prob > 0.5 else "Safe"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))