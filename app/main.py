from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # <-- Import this
from fastapi.responses import FileResponse # <-- Import this
from app.core.config import settings
from app.api.v1.endpoints import prediction
from app.db.session import engine, Base # <-- Import Engine & Base
from app.db_models import user, prediction as prediction_model # <-- Import models to register them
from app.api.v1.endpoints import prediction, auth  # <--- Add auth here
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# 1. Mount the API Router
app.include_router(prediction.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"]) # <--- New Router
# 2. Mount Static Files (CSS, JS, Images)
# أي ملف داخل مجلد static يمكن الوصول له عبر الرابط /static/...
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 3. Serve HTML Pages
@app.get("/")
async def read_index():
    # عند الدخول للصفحة الرئيسية، نعرض الـ Landing Page
    return FileResponse('app/static/index.html')

@app.get("/predict-page")
async def read_predict_page():
    # رابط صفحة التوقع
    return FileResponse('app/static/predict.html')
@app.get("/login-page")
async def login_page():
    return FileResponse('app/static/login.html')

@app.get("/signup-page")
async def signup_page():
    return FileResponse('app/static/signup.html')

@app.get("/dashboard-page")
async def dashboard_page():
    return FileResponse('app/static/dashboard.html')