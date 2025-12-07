from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EstateIQ API"
    PROJECT_VERSION: str = "1.0.0"
    
    # سنستخدم هذا لاحقاً لتحديد البيئة (dev/prod)
    ENVIRONMENT: str = "development" 
    
    DATABASE_URL: str
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # التوكن ينتهي بعد 30 دقيقة
    class Config:
        # Pydantic will read uppercase variables from .env file automatically
        env_file = ".env"

# Instance creation
settings = Settings()