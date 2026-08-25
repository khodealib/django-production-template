# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Features

- **Django {{ cookiecutter.django_version }}** (LTS) with Python {{ cookiecutter.python_version }}
- **uv** for fast dependency management
- **ruff** for linting and formatting
- **mypy** + **django-stubs** for type checking
- **Docker** + **docker-compose** for local and production
- **DevContainer** support for VS Code / GitHub Codespaces
- **PostgreSQL** with health checks
- **Redis** for caching and Celery broker
- **Celery** with django-celery-beat for async tasks and scheduled jobs
- **Django REST Framework** + **drf-spectacular** for API development
- **pytest** + **factory_boy** for testing with reusable fixtures
- **Pre-commit hooks** for code quality
- **GitHub Actions CI** for linting, type checking, and testing
- **Database seeding** command
- **12-Factor** settings via django-environ

## Quick Start

### Using uv (recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

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

### Using Docker

```bash
# Copy environment file
cp .envs/.local .envs/.env

# Start the development stack
make up
# or
docker compose -f compose/local/docker-compose.yml up
```

The development server will be available at http://localhost:8000

## Available Make Commands

```bash
make help          # Show all available commands
make up            # Start local dev stack
make down          # Stop local dev stack
make migrate       # Run migrations
make seed          # Seed database with sample data
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linter
make lint-fix      # Run linter with auto-fix
make format        # Format code
make typecheck     # Run type checker
make shell         # Open Django shell
make pre-commit    # Run pre-commit on all files
```

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── .devcontainer/          # VS Code DevContainer config
├── .envs/                  # Environment variable files
├── compose/                # Docker compose files
│   ├── local/              # Local development
│   └── production/         # Production
├── config/                 # Django project config
│   ├── settings/           # Split settings (base, local, production, test)
│   ├── celery_app.py       # Celery configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI entry point
├── src/                    # Application code
│   └── users/              # Users app (custom user model, seed_data command)
├── tests/                  # Global test fixtures and factories
├── manage.py               # Django management entry point
├── pyproject.toml          # All tool config (uv, ruff, mypy, pytest)
├── Makefile                # Development commands
└── Procfile                # Process manager (Heroku / etc.)
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov --cov-report=term-missing

# Run specific test file
uv run pytest src/users/tests/test_models.py

# Run tests matching a pattern
uv run pytest -k "test_create"
```

## Code Quality

```bash
# Lint
uv run ruff check .

# Lint with auto-fix
uv run ruff check --fix .

# Format
uv run ruff format .

# Type check
uv run mypy .

# Pre-commit (runs all hooks)
uv run pre-commit run --all-files
```

## Development

### Database Seeding

```bash
# Seed with default count (10 users)
uv run python manage.py seed_data

# Seed with custom count
uv run python manage.py seed_data --count 50

# Flush and re-seed
uv run python manage.py seed_data --flush
```

### Adding a New App

```bash
uv run python manage.py startapp myapp src/myapp
```

Then add `"src.myapp"` to `INSTALLED_APPS` in `config/settings/base.py`.

## Deployment

See `compose/production/` for the production Docker setup. Key points:

1. Copy `.envs/.production` to `.envs/.env` and fill in production values
2. Build and run: `docker compose -f compose/production/docker-compose.yml up -d`
3. Run migrations inside the container
4. Collect static files
5. Create a superuser

## License

{{ cookiecutter.license }}
