from fastapi import FastAPI
from app.core.config import settings

# Initialize the app with settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Health Check Endpoint
# Ops Tip: هذا الرابط تستخدمه خدمات الكلاود (AWS Load Balancer) 
# للتأكد من أن السيرفر حي يعمل
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get("/")
def root():
    return {"message": "Welcome to EstateIQ API - Real Estate Pricing Engine"}