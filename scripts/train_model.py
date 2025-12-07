import sys
import os
import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# 1. Setup Paths
# نقوم بتحديد المسار الجذري للمشروع لضمان حفظ الموديل في المكان الصحيح بغض النظر عن مكان تشغيل السكريبت
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# تأكد من وجود مجلد models
os.makedirs(MODELS_DIR, exist_ok=True)

def train():
    print("🚀 Starting training pipeline...")

    # 2. Load Data
    print("📥 Loading California Housing dataset...")
    data = fetch_california_housing()
    X, y = data.data, data.target

    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Train Model
    # نستخدم Random Forest لأنه قوي وسريع ولا يحتاج Scaling معقد
    print("🧠 Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print(f"📊 Model R2 Score: {score:.4f}")

    # 6. Save Model (Serialization)
    model_path = os.path.join(MODELS_DIR, "house_price_model.pkl")
    joblib.dump(model, model_path)
    print(f"💾 Model saved successfully to: {model_path}")

if __name__ == "__main__":
    train()