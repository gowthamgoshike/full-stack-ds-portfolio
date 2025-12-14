import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import sys
import os

# Allow importing from src
sys.path.append(os.getcwd())
from src.features.validate import validate_schema, validate_clean_data

def train():
    print("1. Loading Data...")
    df = pd.read_csv('raw/tested.csv')
    
    # Validation Step 1
    validate_schema(df)
    
    print("2. Cleaning Data...")
    # Fill missing ages with the median (Simulating data cleaning)
    df['Age'] = df['Age'].fillna(df['Age'].median())
    
    # Validation Step 2
    validate_clean_data(df)

    print("3. Training Model...")
    features = ['Pclass', 'SibSp', 'Parch', 'Age']
    X = df[features]
    y = df['Survived'] # tested.csv has this column
    
    model = DecisionTreeClassifier(max_depth=4)
    model.fit(X, y)
    
    print("4. Saving Model...")
    joblib.dump(model, 'models/decision_tree.pkl')
    print("✅ Success! Model saved.")

if __name__ == "__main__":
    train()