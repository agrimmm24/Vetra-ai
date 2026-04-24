import joblib
import os
import numpy as np
from backend.config import settings

class PredictionService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """
        Attempts to load the trained ML model from disk.
        Falls back to dummy mode if model is missing.
        """
        if os.path.exists(settings.MODEL_PATH):
            try:
                self.model = joblib.load(settings.MODEL_PATH)
                print(f"ML Model loaded successfully from {settings.MODEL_PATH}")
            except Exception as e:
                print(f"Error loading model: {e}. Falling back to mock mode.")
                self.model = None
        else:
            print(f"Model file not found at {settings.MODEL_PATH}. Running in mock mode.")
            self.model = None

    def predict(self, feature_vector: np.ndarray) -> float:
        """
        Runs inference on the feature vector.
        Returns a risk probability / score scaled 0-100.
        """
        if self.model:
            # Assuming a classifier with predict_proba
            try:
                # Get probability for 'sick' (class 1)
                prob = self.model.predict_proba(feature_vector)[0][1]
                return float(prob * 100)
            except Exception as e:
                print(f"Prediction error: {e}")
                return self._mock_predict(feature_vector)
        else:
            return self._mock_predict(feature_vector)

    def _mock_predict(self, feature_vector: np.ndarray) -> float:
        """
        Fallback logic that mimics ML behavior when no model is present.
        """
        # Features: [milk_drop_pct, feed_score, activity_score, temp_risk, temp_deviation, ph_score, hr_score]
        v = feature_vector[0]
        # Simulate a score based on feature intensity
        score = (v[0] * 20 + (1-v[1]) * 15 + (1-v[2]) * 15 + v[3] * 20 + v[5] * 15 + v[6] * 15)
        return min(100.0, max(0.0, float(score)))

prediction_service = PredictionService()
