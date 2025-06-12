# -------- Base stage --------
FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y openssl nano sudo && \
    mkdir -p /app/certs

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/

COPY cert_gen.sh /cert_gen.sh
RUN chmod +x /cert_gen.sh && /cert_gen.sh

# ---------------------------

# -------- Dev stage --------
FROM base AS dev

RUN apt-get update && apt-get install -y sqlite3 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY load_sqlite3.sh /load_sqlite3.sh
COPY entrypoint_dev.sh /entrypoint.sh
RUN chmod +x /load_sqlite3.sh /entrypoint.sh

COPY --from=base /app/certs /app/certs

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "run.py"]

# -------- Prod stage --------
FROM base AS prod

COPY --from=base /app/certs /app/certs

CMD ["python", "run.py"]