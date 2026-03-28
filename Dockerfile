# Build context: repository root (see docs/CLOUDRUN.md).
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY src/backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY src/backend/ /app/backend/
COPY src/frontend/ /app/frontend/

WORKDIR /app/backend
CMD ["python", "main.py"]
