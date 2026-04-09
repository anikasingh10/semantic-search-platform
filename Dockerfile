FROM python:3.10

WORKDIR /app

# Copy only requirements first (for caching)
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Then copy full backend code
COPY backend/ .

CMD ["python", "app/main.py"]