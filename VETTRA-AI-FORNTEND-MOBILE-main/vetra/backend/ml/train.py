import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import os

def generate_synthetic_data(samples=10000):
    """
    Generates synthetic livestock health data for training with more features.
    """
    print(f"Generating {samples} realistic samples with extended features...")
    np.random.seed(42)
    
    # Features
    milk_drop = np.random.uniform(0, 0.4, samples)
    feed = np.random.choice([0, 0.5, 1.0], samples)
    activity = np.random.choice([0, 0.5, 1.0], samples)
    
    # Temperature (38.5C is typical, dev > 1.5 is risky)
    temp_base = 38.5
    temp_vals = np.random.normal(temp_base, 1.2, samples)
    temp_vals = np.clip(temp_vals, 35.0, 42.0)
    temp_deviation = np.abs(temp_vals - temp_base)
    temp_risk = (temp_deviation > 1.0).astype(float)
    
    # pH (Normal 6.4 - 6.8)
    ph_vals = np.random.normal(6.6, 0.4, samples)
    ph_vals = np.clip(ph_vals, 4.0, 9.0)
    ph_score = (np.abs(ph_vals - 6.6) / 1.0).clip(0, 1)
    
    # Heart Rate (Normal 60-80)
    hr_vals = np.random.normal(70, 15, samples)
    hr_vals = np.clip(hr_vals, 40, 140)
    hr_score = (np.abs(hr_vals - 70) / 40.0).clip(0, 1)
    
    # Label logic: 
    # Sick if (temp high AND milk drop) OR (feed low AND activity low) OR (high ph OR high hr)
    is_sick = (
        ((milk_drop > 0.15) & (temp_risk == 1.0)) | 
        ((feed <= 0.5) & (activity <= 0.5) & (temp_deviation > 0.5)) |
        (ph_score > 0.6) | 
        (hr_score > 0.7) |
        (temp_deviation > 1.8)
    ).astype(int)
    
    # Add some noise (3%)
    noise = np.random.choice([0, 1], samples, p=[0.97, 0.03])
    is_sick = np.where(noise == 1, 1 - is_sick, is_sick)
    
    df = pd.DataFrame({
        "milk_drop_pct": milk_drop,
        "feed_score": feed,
        "activity_score": activity,
        "temp_risk": temp_risk,
        "temp_deviation": temp_deviation / 2.0,
        "ph_score": ph_score,
        "hr_score": hr_score,
        "is_sick": is_sick
    })
    
    return df

def train_models():
    print("Preparing upgraded dataset (10,000 samples)...")
    df = generate_synthetic_data(10000)
    
    # Save dataset
    os.makedirs("backend/ml/dataset", exist_ok=True)
    df.to_csv("backend/ml/dataset/synthetic_data.csv", index=False)
    
    X = df.drop("is_sick", axis=1)
    y = df["is_sick"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # XGBoost Classifier
    print("Training XGBoost Classifier...")
    xgb = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    xgb.fit(X_train, y_train)
    
    # Evaluation
    print("\nXGBoost Performance Report:")
    print(classification_report(y_test, xgb.predict(X_test)))
    
    # Save Model
    os.makedirs("backend/models/trained", exist_ok=True)
    joblib.dump(xgb, "backend/models/trained/random_forest_model.pkl") # Kept same name for backend compatibility
    print("\nModel saved to backend/models/trained/random_forest_model.pkl (XGBoost)")

if __name__ == "__main__":
    train_models()
