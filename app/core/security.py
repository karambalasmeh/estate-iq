from datetime import datetime, timedelta
from typing import Optional
from jose import jwt # هذه المكتبة التي ثبتناها سابقاً
from app.core.config import settings
from passlib.context import CryptContext
# نحدد نوع التشفير (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    تتأكد هل الباسورد الذي أدخله المستخدم يطابق المشفر في الداتا بيس
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    تأخذ الباسورد العادي وترجع خربشات (Hash)
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    تقوم بإنشاء توكن مشفر يحتوي على بيانات المستخدم
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # نضيف وقت الانتهاء للبيانات
    to_encode.update({"exp": expire})
    
    # التشفير
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt