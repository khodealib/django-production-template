FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

FROM base AS dev

# Non-root dev user expected by .devcontainer/devcontainer.json (remoteUser)
RUN useradd -m -s /bin/bash vscode

COPY pyproject.toml ./
RUN uv sync --no-install-project

COPY . .
RUN uv sync

USER vscode
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
