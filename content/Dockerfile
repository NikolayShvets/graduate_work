FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    PYTHONPATH='/app'

WORKDIR /app

RUN pip install --upgrade pip
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --no-directory --no-interaction

COPY . .
