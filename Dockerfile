# -------- Base stage --------
FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y openssl nano sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/

CMD ["python", "run.py"]