from sqlalchemy.orm import Session
from app.db_models.user import User  # لاحظ استخدام db_models
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """يبحث عن مستخدم بواسطة الإيميل"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """ينشئ مستخدم جديد مع تشفير كلمة السر"""
    
    # 1. Hash the password
    hashed_password = get_password_hash(user.password)
    
    # 2. Create DB Object
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    # 3. Add & Commit
    db.add(db_user)
    db.commit()
    
    # 4. Refresh to get the ID and created_at from DB
    db.refresh(db_user)
    return db_user