FROM python:3.11-slim

# Ortam değişkenleri ve çalışma dizini
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Netcat (doğru paket: netcat-openbsd) ve pip paketleri yükleniyor
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Gereksinimler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY ./app /app

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
