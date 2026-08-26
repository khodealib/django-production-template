FROM python:{{ cookiecutter.python_version }}-slim AS builder

# uv is the only package manager used in this project
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

# Use the image's Python; never download a managed interpreter
ENV UV_PYTHON_DOWNLOADS=0
# Cache and target live on different file systems during builds
ENV UV_LINK_MODE=copy
# Compile bytecode for faster startup in production
ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev --group production

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --group production

FROM python:{{ cookiecutter.python_version }}-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r {{ cookiecutter.project_slug }} && \
    useradd -r -g {{ cookiecutter.project_slug }} -d /app -s /sbin/nologin {{ cookiecutter.project_slug }}

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN chown -R {{ cookiecutter.project_slug }}:{{ cookiecutter.project_slug }} /app

USER {{ cookiecutter.project_slug }}

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
