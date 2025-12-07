from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # الربط مع المستخدم (Foreign Key)
    # نقول له: هذا العمود مرتبط بعمود id في جدول users
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # تخزين مدخلات التوقع (الغرف، المساحة، الخ) كـ JSON كامل
    # مثال: {"MedInc": 3.5, "HouseAge": 25, ...}
    input_data = Column(JSON, nullable=False)
    
    # السعر الذي توقعه الموديل
    predicted_price = Column(Float, nullable=False)
    
    # متى حدث هذا التوقع؟
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # العلاقة العكسية: للوصول لمعلومات صاحب التوقع عبر prediction.owner
    owner = relationship("User", back_populates="predictions")