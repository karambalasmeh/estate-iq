from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.house import HouseFeatures, PricePrediction
from app.services.model_service import model_service
from app.db.session import get_db
from app.api.v1.endpoints.deps import get_current_user
from app.db_models.user import User
from app.db_models.prediction import Prediction # استيراد موديل الداتا بيس
from app.schemas.prediction import PredictionResponse # Import this
from typing import List
router = APIRouter()

@router.post("/predict", response_model=PricePrediction)
def predict_house_price(
    features: HouseFeatures,
    db: Session = Depends(get_db),        # نحتاج الداتا بيس للحفظ
    current_user: User = Depends(get_current_user) # نحتاج المستخدم الحالي (محمية)
):
    """
    Predict house price and save to history.
    **Requires Authentication**
    """
    try:
        # 1. AI Prediction
        # تحويل مدخلات المستخدم لقائمة يفهمها الموديل
        input_list = [
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude
        ]
        
        predicted_value = model_service.predict(input_list)
        
        # 2. Save to Database
        # نحول المدخلات لـ Dictionary لنخزنها كـ JSON
        input_json = features.model_dump() 
        
        db_prediction = Prediction(
            user_id=current_user.id,      # ربط التوقع بالمستخدم الحالي
            input_data=input_json,        # تخزين المدخلات
            predicted_price=predicted_value # تخزين النتيجة
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction) # (اختياري) لجلب الـ ID الجديد
        
        # 3. Return Result
        return PricePrediction(predicted_price=predicted_value)

    except Exception as e:
        print(f"Error: {e}") # For debugging
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/history", response_model=List[PredictionResponse])
def read_user_history(
    current_user: User = Depends(get_current_user)
):
    """
    Get all previous predictions for the logged-in user.
    """
    # بفضل العلاقة التي بنيناها في SQLAlchemy، يمكننا جلب التوقعات هكذا ببساطة:
    return current_user.predictions
from sqlalchemy import func

@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get simple analytics for the user.
    """
    # عدد التوقعات الكلي للمستخدم
    total_predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).count()
    
    # متوسط الأسعار التي توقعها المستخدم
    avg_price = db.query(func.avg(Prediction.predicted_price)).filter(Prediction.user_id == current_user.id).scalar() or 0.0
    
    return {
        "total_predictions": total_predictions,
        "average_predicted_price": avg_price,
        "user_name": current_user.full_name
    }