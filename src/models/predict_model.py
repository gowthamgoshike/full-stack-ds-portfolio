import pandas as pd
import joblib

def make_predictions():
    # 1. Load the compiled model
    print("Loading model from 'models/decision_tree.pkl'...")
    model = joblib.load('models/decision_tree.pkl')
    
    # 2. Load the data
    # (In a real project, this would be new data without the answers)
    print("Loading data...")
    df = pd.read_csv('data/data.csv')
    
    # 3. Select the EXACT same features we trained on
    features = ['Pclass', 'SibSp', 'Parch']
    X_new = df[features]
    
    # 4. Make Predictions
    print("Generating predictions...")
    predictions = model.predict(X_new)
    
    # 5. Add predictions back to the DataFrame to see them
    df['Predicted_Survived'] = predictions
    
    # Show the first 10 results
    print("\n--- Prediction Results ---")
    print(df[['PassengerId', 'Pclass', 'Predicted_Survived']].head(10))
    
    # Optional: Save results to a CSV
    # df.to_csv('data/predictions.csv', index=False)

if __name__ == '__main__':
    make_predictions()