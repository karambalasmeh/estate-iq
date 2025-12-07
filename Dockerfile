# -----------------------------------------------------------
# Stage 1: Builder (المرحلة التحضيرية)
# نستخدم نسخة كاملة لنبني المكتبات ونحمل كل شيء
# -----------------------------------------------------------
FROM python:3.13-slim as builder

# منع بايثون من كتابة ملفات .pyc وتقليل حجم اللوج
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# تثبيت أدوات النظام اللازمة للبناء (مثل gcc لمكتبات الداتا بيس)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# تحضير البيئة الافتراضية
RUN python -m venv /opt/venv
# تفعيل البيئة في المسار (PATH)
ENV PATH="/opt/venv/bin:$PATH"

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------
# Stage 2: Final Runtime (مرحلة التشغيل الخفيفة)
# نأخذ نسخة slim نظيفة وننقل لها ما جهزناه فقط
# -----------------------------------------------------------
FROM python:3.13-slim

# إعدادات لتقليل المشاكل
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# إضافة البيئة الافتراضية للمسار لكي يراها النظام فوراً
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# نسخ البيئة الافتراضية الجاهزة من المرحلة الأولى (builder)
COPY --from=builder /opt/venv /opt/venv

# نسخ كود المشروع بالكامل
COPY . .

# فتح المنفذ (للتوثيق فقط)
EXPOSE 8000

# أمر التشغيل النهائي
# نستخدم 0.0.0.0 لنسمح بالوصول من خارج الحاوية
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]