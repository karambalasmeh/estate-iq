from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.services.auth_service import get_user_by_email
from app.db_models.user import User

# هذا يخبر FastAPI أن التوكن سيأتي في الهيدر بعنوان Authorization: Bearer ...
# ويضع زر القفل في الـ Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    هذه الدالة هي الحارس.
    إذا كان التوكن سليم -> ترجع كائن المستخدم.
    إذا كان التوكن مزور أو منتهي -> ترمي خطأ 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. فك تشفير التوكن
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # 2. التأكد أن المستخدم موجود في الداتا بيس
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user