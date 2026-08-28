# Django Production Template

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for jumpstarting production-ready Django projects with modern tooling.

**Python 3.13** · **Django 5.2 LTS** · **uv** · **mypy strict** · **DevContainer** · **drf-spectacular** · **GitHub Actions CI**

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Django Version](https://img.shields.io/badge/django-5.2%20LTS-green.svg)](https://www.djangoproject.com/download/)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type_checked-mypy-blue.svg)](https://mypy-lang.org/)

## Why this template?

| Feature | django-cookiecutter | cookiecutter-django | **This template** |
|---------|---------------------|---------------------|-------------------|
| Package manager | pip/poetry | pip/poetry | **uv** (10-100x faster) |
| Type checking | Optional | Optional | **mypy strict + django-stubs** |
| DevContainer | ❌ | ❌ | **VS Code / Codespaces ready** |
| API schema | drf-yasg (deprecated) | drf-yasg | **drf-spectacular** (maintained) |
| Settings | Split | Split | **Split + django-environ** |
| CI/CD | GitHub Actions | GitHub Actions | **ruff → format → mypy → pytest** |
| Response envelope | ❌ | ❌ | **Typed DRF envelope contract** |
| Pagination tests | ❌ | ❌ | **Full coverage matrix** |
| Database seeding | ❌ | ✅ | **Custom management command** |
| Python version | 3.11 | 3.11 | **3.13** |
| Django version | 4.2/5.0 | 4.2/5.0 | **5.2 LTS** |

## Features

- **Django 5.2 LTS** + **Python 3.13**
- **uv** for dependency management (10-100x faster than pip)
- **ruff** for linting and formatting (replaces flake8, black, isort)
- **mypy** + **django-stubs** for strict type checking
- **Docker** + **docker-compose** for local and production
- **DevContainer** support for VS Code / GitHub Codespaces
- **PostgreSQL** + **Redis** + **Celery** with django-celery-beat
- **Django REST Framework** + **drf-spectacular** for OpenAPI 3 schemas
- **pytest** + **factory_boy** for testing with reusable fixtures
- **Pre-commit hooks** (ruff, mypy, check-yaml, etc.)
- **GitHub Actions CI** (lint → format → typecheck → test)
- **Database seeding** command with factories
- **12-Factor** settings via django-environ
- **Typed API response envelope** (success, pagination, data, errors) with drf-spectacular integration

## Quick Start

```bash
# Install cookiecutter via uv
uv tool install cookiecutter

# Generate a project
cookiecutter https://github.com/khodealib/django-production-template
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `project_name` | My Project | Human-readable project name |
| `project_slug` | my_project | Python-importable slug |
| `description` | A short description | Project description |
| `author_name` | Your Name | Author name |
| `email` | you@example.com | Author email |
| `version` | 0.1.0 | Initial version |
| `license` | MIT | Software license (MIT, BSD-3-Clause, Apache-2.0, GPL-3.0, Not open source) |
| `timezone` | UTC | Django timezone |
| `python_version` | 3.13 | Python version |
| `django_version` | 5.2 | Django version |
| `postgresql_version` | 17 | PostgreSQL version |
| `redis_version` | 7 | Redis version |

## Generated Project Structure

After running cookiecutter, you get a ready-to-run Django project:

```
my_project/
├── .devcontainer/              # VS Code DevContainer config
│   ├── devcontainer.json
│   └── docker-compose.yml
├── .envs/                      # Environment variable files
│   ├── .local                  # Local development (copied to .env)
│   ├── .production             # Production template (deleted post-gen)
│   └── .test                   # Test environment (deleted post-gen)
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI (ruff → format → mypy → pytest)
├── compose/                    # Docker compose files
│   ├── local/                  # Local development stack
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── celery/start
│   └── production/             # Production stack
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── celery/start
├── config/                     # Django project config
│   ├── settings/
│   │   ├── base.py             # Base settings (all envs)
│   │   ├── local.py            # Local overrides
│   │   ├── production.py       # Production overrides
│   │   └── test.py             # Test overrides
│   ├── celery_app.py           # Celery configuration
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI entry point
├── src/                        # Application code (Python packages)
│   ├── common/                 # Shared utilities
│   │   ├── pagination.py       # EnvelopePageNumberPagination
│   │   ├── views.py            # EnvelopeModelViewSet
│   │   ├── exceptions.py       # envelope_exception_handler
│   │   └── spectacular.py      # EnvelopeAutoSchema for drf-spectacular
│   └── users/                  # Users app (custom user model)
│       ├── models.py           # Custom User model
│       ├── views.py            # UserViewSet with envelope
│       ├── serializers.py
│       ├── services.py         # Business logic
│       ├── selectors.py        # Read operations
│       ├── tasks.py            # Celery tasks
│       ├── factories.py        # factory_boy factories
│       ├── tests/              # Co-located tests
│       │   ├── test_models.py
│       │   ├── test_views.py
│       │   ├── test_services.py
│       │   └── test_api_schema.py
│       └── management/commands/
│           └── seed_data.py    # Database seeding command
├── tests/                      # Global test fixtures
│   └── factories.py
├── static/                     # Static files (.gitkeep)
├── manage.py                   # Django management entry point
├── pyproject.toml              # All tool config (uv, ruff, mypy, pytest, hatch)
├── Makefile                    # Development commands
├── Procfile                    # Process manager (Heroku, etc.)
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .dockerignore
├── .editorconfig
├── .gitignore
├── AGENTS.md                   # AI agent guidance
├── LICENSE
└── README.md                   # This file (generated)
```

## Template Verification (CI)

This repo tests the template by rendering it and asserting on the output:

```bash
# Run template verification tests
uv sync && uv run pytest
```

This renders the template via `cookiecutter --no-input` into a temp directory and runs 50+ assertions on the generated structure, Dockerfiles, settings, CI config, and the API envelope contract.

## Usage in Generated Project

Once you've generated a project, use the Makefile for common tasks:

```bash
# Install dependencies
make install          # uv sync

# Docker development stack
make up               # Start postgres, redis, web, celery
make down             # Stop stack

# Database
make migrate          # Run migrations
make seed             # Seed database with sample data

# Code quality
make lint             # ruff check
make lint-fix         # ruff check --fix
make format           # ruff format
make typecheck        # mypy

# Testing
make test             # pytest
make test-cov         # pytest with coverage

# Shell access
make shell            # Django shell
make dbshell          # PostgreSQL shell
```

Or with uv directly:

```bash
# Install dependencies
uv sync

# Set up environment
cp .envs/.local .envs/.env

# Run migrations
uv run python manage.py migrate

# Seed the database
uv run python manage.py seed_data

# Start the dev server
uv run python manage.py runserver
```

## Deployment

See `compose/production/` for the production Docker setup:

1. Copy `.envs/.production` to `.envs/.env` and fill in production values
2. Build and run: `docker compose -f compose/production/docker-compose.yml up -d`
3. Run migrations inside the container
4. Collect static files
5. Create a superuser

## Example Generated Project

See a live example: **[django-production-template-example](https://github.com/khodealib/django-production-template-example)** (placeholder — create this repo to showcase a rendered project)

## License

MIT