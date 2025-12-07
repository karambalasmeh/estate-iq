from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import create_user, get_user_by_email
from app.schemas.token import Token # <-- Import Token Schema
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.api.v1.endpoints.deps import get_current_user
from app.schemas.user import UserResponse
from app.db_models.user import User

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # 1. Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # 2. Create user
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # 1. البحث عن المستخدم
    user = get_user_by_email(db, email=form_data.username) # OAuth2 form stores email in 'username' field
    
    # 2. التحقق من المستخدم والباسورد
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. إنشاء التوكن
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, # sub = subject (who is this token for?)
        expires_delta=access_token_expires
    )
    
    # 4. إرجاع التوكن
    return {"access_token": access_token, "token_type": "bearer"}
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current logged-in user details.
    """
    return current_user