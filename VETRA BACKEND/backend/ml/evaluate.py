import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import os

def evaluate():
    data_path = "backend/ml/dataset/synthetic_data.csv"
    if not os.path.exists(data_path):
        print("Dataset not found. Run train.py first.")
        return
        
    df = pd.read_csv(data_path)
    X = df.drop("is_sick", axis=1)
    y = df["is_sick"]
    
    model_path = "backend/models/trained/random_forest_model.pkl"
    if not os.path.exists(model_path):
        print("Model not found. Run train.py first.")
        return
        
    model = joblib.load(model_path)
    predictions = model.predict(X)
    
    print("Model Evaluation Results:")
    print("-" * 30)
    print(classification_report(y, predictions))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, predictions))

if __name__ == "__main__":
    evaluate()
