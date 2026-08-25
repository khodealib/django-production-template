# Django Production Template

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for jumpstarting production-ready Django projects.

## Features

- **Django 5.2 LTS** + **Python 3.13**
- **uv** for dependency management
- **ruff** for linting and formatting
- **mypy** + **django-stubs** for type checking
- **Docker** + **docker-compose** for local and production
- **DevContainer** support for VS Code / GitHub Codespaces
- **PostgreSQL** + **Redis** + **Celery**
- **Django REST Framework** + **drf-spectacular**
- **pytest** + **factory_boy** for testing with reusable fixtures
- **Pre-commit hooks**
- **GitHub Actions CI**
- **Database seeding** command
- **12-Factor** settings via django-environ

## Usage

```bash
# Install cookiecutter
uv tool install cookiecutter

# Generate a project
cookiecutter https://github.com/yourusername/django-production-template
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
| `license` | MIT | Software license |
| `timezone` | UTC | Django timezone |
| `python_version` | 3.13 | Python version |
| `django_version` | 5.2 | Django version |
| `postgresql_version` | 17 | PostgreSQL version |
| `redis_version` | 7 | Redis version |

## License

MIT
