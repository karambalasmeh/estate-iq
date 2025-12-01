from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EstateIQ API"
    PROJECT_VERSION: str = "1.0.0"
    
    # سنستخدم هذا لاحقاً لتحديد البيئة (dev/prod)
    ENVIRONMENT: str = "development" 

    class Config:
        # Pydantic will read uppercase variables from .env file automatically
        env_file = ".env"

# Instance creation
settings = Settings()