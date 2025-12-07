from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    # اسم الجدول كما سيظهر في الداتا بيس
    __tablename__ = "users"

    # الأعمدة
    id = Column(Integer, primary_key=True, index=True) # الرقم المميز
    email = Column(String, unique=True, index=True, nullable=False) # إيميل لا يتكرر
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False) # كلمة السر المشفرة
    is_active = Column(Boolean, default=True) # هل الحساب فعال؟
    
    # التوقيت: يتم وضعه تلقائياً عند الإنشاء
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # العلاقات (Relationships)
    # هذا السطر سحري: يسمح لك بالوصول لكل توقعات المستخدم عبر user.predictions
    predictions = relationship("Prediction", back_populates="owner")