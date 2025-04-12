FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY .env .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]