FROM python:{{ cookiecutter.python_version }}-slim AS base

# uv is the only package manager used in this project
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

# Use the image's Python; never download a managed interpreter
ENV UV_PYTHON_DOWNLOADS=0
# Cache and target live on different file systems during builds
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS dev

# Non-root dev user expected by .devcontainer/devcontainer.json (remoteUser)
RUN useradd -m -s /bin/bash vscode

COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

USER vscode
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
