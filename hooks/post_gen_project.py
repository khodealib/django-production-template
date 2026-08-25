"""Post-generation hook for cookiecutter-django-production-template."""

import secrets
import stat
import string
from pathlib import Path


def generate_secret_key() -> str:
    """Generate a Django-compatible secret key."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for _ in range(50))


def make_executable(path: Path) -> None:
    """Make a file executable."""
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def main() -> None:
    secret_key = generate_secret_key()

    envs_local = Path(".envs/.local")
    envs_local.write_text(
        envs_local.read_text().replace("CHANGE_ME_SECRET_KEY", secret_key)
    )

    celery_start = Path("compose/local/celery/start")
    if celery_start.exists():
        make_executable(celery_start)

    celery_start_prod = Path("compose/production/celery/start")
    if celery_start_prod.exists():
        make_executable(celery_start_prod)

    Path(".envs/.production").unlink(missing_ok=True)
    Path(".envs/.test").unlink(missing_ok=True)

    print()  # noqa: T201
    print(  # noqa: T201
        "---------------------------------------------------------------\n"
        "Django project created successfully!\n\n"
        "Next steps:\n"
        "  1. cd {{ cookiecutter.project_slug }}\n"
        "  2. uv sync\n"
        "  3. cp .envs/.local .envs/.env\n"
        "  4. uv run python src/{{ cookiecutter.project_slug }}/manage.py migrate\n"
        "  5. uv run python src/{{ cookiecutter.project_slug }}/manage.py seed_data\n"
        "  6. uv run python src/{{ cookiecutter.project_slug }}/manage.py runserver\n\n"
        "Or with Docker:\n"
        "  1. cd {{ cookiecutter.project_slug }}\n"
        "  2. cp .envs/.local .envs/.env\n"
        "  3. make up\n"
        "---------------------------------------------------------------"
    )


if __name__ == "__main__":
    main()
