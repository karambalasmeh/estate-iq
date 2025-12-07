import joblib
import os
import numpy as np
from app.core.config import settings

class HousePriceModel:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join("models", "house_price_model.pkl")
        self.load_model()

    def load_model(self):
        """Loads the model from disk if it exists."""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"✅ Model loaded successfully from {self.model_path}")
            else:
                print(f"⚠️ Warning: Model file not found at {self.model_path}. Please run training script.")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

    def predict(self, features: list) -> float:
        """
        Takes a list of features and returns a prediction.
        """
        if not self.model:
            raise RuntimeError("Model is not loaded")
        
        # Scikit-learn expects a 2D array
        features_array = np.array([features])
        prediction = self.model.predict(features_array)
        return float(prediction[0])

# Singleton Pattern: Create one instance to be used everywhere
# Ops Tip: هذا يمنع تحميل الموديل مع كل Request مما يوفر الرام والوقت
model_service = HousePriceModel()