FROM python:3.11-slim

# Ortam değişkenleri ve çalışma dizini
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Gereksinimler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY ./app /app

# Uvicorn ile sunucu başlatma
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
