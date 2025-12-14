import pandas as pd

def validate_schema(df):
    """Checks if the raw data has the right columns."""
    required_cols = ['Pclass', 'SibSp', 'Parch', 'Age']
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        raise ValueError(f"Data Error: Missing columns {missing}")
    return True

def validate_clean_data(df):
    """Checks for logical errors (like negative ages)."""
    if (df['Age'] < 0).any():
        raise ValueError("Data Error: Found negative values in 'Age'.")
    return True