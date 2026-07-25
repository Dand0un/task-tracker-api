# syntax=docker/dockerfile:1

# ---- Builder stage: install dependencies into a venv ----
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---- Runtime stage: minimal image with just the venv + app code ----
FROM python:3.11-slim AS runtime

# Non-root user to run the app as
RUN useradd --create-home --shell /usr/sbin/nologin app

# Bring in the pre-built dependencies (no pip/build tools in this stage)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Only the runtime application package is copied in
COPY app ./app

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
