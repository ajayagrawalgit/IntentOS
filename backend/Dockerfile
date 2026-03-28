# Use the official slim Python image for performance and security
FROM python:3.11-slim

# Set non-interactive environment variables and buffering
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# Set the working directory in the container
WORKDIR /app

# Install simple system requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (use no-cache to keep the image small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend into the container (including the nested frontend folder)
COPY . .

# Ensure the app starts with the standard PORT-binding logic
CMD ["python", "main.py"]