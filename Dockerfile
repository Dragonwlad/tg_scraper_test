FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYTHONPATH="/app" \
    APP_PATH="/app" \
    VENV_PATH="/app/.venv"

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-root


# Открытие порта (если нужно)
#EXPOSE 8000
