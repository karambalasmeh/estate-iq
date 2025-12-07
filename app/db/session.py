from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Create Engine
# المحرك هو المسؤول عن التحدث مع الداتا بيس
engine = create_engine(settings.DATABASE_URL)

# 2. SessionLocal
# هذا المصنع الذي سينتج لنا "جلسات" اتصال
# كل طلب (Request) من مستخدم سيحصل على جلسة خاصة به
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base Class
# أي موديل (جدول) سننشئه لاحقاً سيرث من هذا الكلاس
Base = declarative_base()

# 4. Dependency Injection
# هذه الدالة سنستخدمها في كل Endpoint يحتاج داتا بيس
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()