import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

def train():
    # 1. Load the data
    # We assume the file is stored in 'data/raw/'
    print("Loading data...")
    df = pd.read_csv('data/data.csv')

    # 2. Select Features (X) and Target (y)
    # We are selecting only the numeric columns that have no missing values
    features = ['Pclass', 'SibSp', 'Parch']
    
    X = df[features]
    y = df['Survived']
    
    print(f"Training on features: {features}")

    # 3. Train the Model
    print("Training model...")
    # We limit depth to 4 to keep the tree simple and interpretable
    model = DecisionTreeClassifier(max_depth=4)
    model.fit(X, y)

    # 4. Save the Model
    print("Saving model...")
    joblib.dump(model, 'models/decision_tree.pkl')
    print("Success! Model saved to 'models/decision_tree.pkl'")

if __name__ == '__main__':
    train()