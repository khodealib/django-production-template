FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

FROM base AS dev

COPY pyproject.toml ./
RUN uv sync --no-install-project

COPY . .
RUN uv sync

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
