FROM python:{{ cookiecutter.python_version }}-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-install-project --no-dev

COPY . .

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
