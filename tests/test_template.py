"""Tests for the cookiecutter template."""

import os
import subprocess
from pathlib import Path

import pytest

RENDERED_PROJECT = Path("output/my_project")


@pytest.fixture(scope="session")
def rendered_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Render the cookiecutter template once for all tests."""
    tmp = tmp_path_factory.mktemp("output")
    subprocess.run(
        [
            "cookiecutter",
            "--no-input",
            "--output-dir",
            str(tmp),
            str(Path(__file__).parent.parent),
        ],
        check=True,
        cwd=str(tmp),
    )
    project = tmp / "my_project"
    assert project.exists(), f"Project not found at {project}"
    return project


class TestProjectStructure:
    def test_pyproject_toml_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "pyproject.toml").exists()

    def test_makefile_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "Makefile").exists()

    def test_procfile_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "Procfile").exists()

    def test_readme_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "README.md").exists()

    def test_license_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "LICENSE").exists()

    def test_gitignore_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".gitignore").exists()

    def test_editorconfig_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".editorconfig").exists()

    def test_precommit_config_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".pre-commit-config.yaml").exists()

    def test_agents_md_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "AGENTS.md").exists()

    def test_manage_py_at_root(self, rendered_project: Path) -> None:
        assert (rendered_project / "manage.py").exists()
        assert not (rendered_project / "src" / "my_project").exists()

    def test_static_dir_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "static" / ".gitkeep").exists()


class TestDevContainer:
    def test_devcontainer_json_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".devcontainer" / "devcontainer.json").exists()

    def test_devcontainer_compose_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".devcontainer" / "docker-compose.yml").exists()


class TestDocker:
    def test_local_dockerfile_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "local" / "Dockerfile").exists()

    def test_local_compose_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "local" / "docker-compose.yml").exists()

    def test_production_dockerfile_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "production" / "Dockerfile").exists()

    def test_production_compose_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "production" / "docker-compose.yml").exists()

    def test_celery_worker_local_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "local" / "celery" / "start").exists()

    def test_celery_worker_prod_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "compose" / "production" / "celery" / "start").exists()

    def test_local_dockerfile_creates_dev_user(self, rendered_project: Path) -> None:
        content = (rendered_project / "compose" / "local" / "Dockerfile").read_text()
        assert "useradd" in content and "vscode" in content
        assert "USER vscode" in content


class TestDjangoConfig:
    def test_settings_base_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "settings" / "base.py").exists()

    def test_settings_local_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "settings" / "local.py").exists()

    def test_settings_production_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "settings" / "production.py").exists()

    def test_settings_test_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "settings" / "test.py").exists()

    def test_celery_app_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "celery_app.py").exists()

    def test_urls_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "urls.py").exists()

    def test_wsgi_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "config" / "wsgi.py").exists()


class TestUsersApp:
    def test_models_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "models.py").exists()

    def test_initial_migration_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "migrations" / "0001_initial.py").exists()

    def test_factories_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "factories.py").exists()

    def test_views_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "views.py").exists()

    def test_serializers_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "serializers.py").exists()

    def test_services_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "services.py").exists()

    def test_selectors_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "selectors.py").exists()

    def test_tasks_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "tasks.py").exists()

    def test_admin_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "admin.py").exists()


class TestTests:
    def test_root_conftest_exists(self, rendered_project: Path) -> None:
        # must live at project root so pytest loads it for src/<app>/tests too
        assert (rendered_project / "conftest.py").exists()

    def test_global_factories_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / "tests" / "factories.py").exists()

    def test_user_tests_exist(self, rendered_project: Path) -> None:
        assert (rendered_project / "src" / "users" / "tests" / "test_models.py").exists()
        assert (rendered_project / "src" / "users" / "tests" / "test_views.py").exists()
        assert (rendered_project / "src" / "users" / "tests" / "test_services.py").exists()

    def test_seed_command_exists(self, rendered_project: Path) -> None:
        assert (
            rendered_project / "src" / "users" / "management" / "commands" / "seed_data.py"
        ).exists()


class TestCI:
    def test_github_actions_ci_exists(self, rendered_project: Path) -> None:
        assert (rendered_project / ".github" / "workflows" / "ci.yml").exists()


class TestContent:
    def test_pyproject_has_uv_deps(self, rendered_project: Path) -> None:
        content = (rendered_project / "pyproject.toml").read_text()
        assert "django" in content
        assert "djangorestframework" in content
        assert "celery" in content
        assert "psycopg" in content

    def test_pyproject_has_ruff_config(self, rendered_project: Path) -> None:
        content = (rendered_project / "pyproject.toml").read_text()
        assert "[tool.ruff]" in content

    def test_pyproject_has_mypy_config(self, rendered_project: Path) -> None:
        content = (rendered_project / "pyproject.toml").read_text()
        assert "[tool.mypy]" in content
        assert "mypy_django_plugin.main" in content

    def test_pyproject_has_pytest_config(self, rendered_project: Path) -> None:
        content = (rendered_project / "pyproject.toml").read_text()
        assert "[tool.pytest.ini_options]" in content

    def test_settings_uses_enviroh(self, rendered_project: Path) -> None:
        content = (rendered_project / "config" / "settings" / "base.py").read_text()
        assert "django-environ" in content or "import environ" in content

    def test_settings_has_auth_user_model(self, rendered_project: Path) -> None:
        content = (rendered_project / "config" / "settings" / "base.py").read_text()
        assert 'AUTH_USER_MODEL = "users.User"' in content

    def test_dockerfile_uses_uv(self, rendered_project: Path) -> None:
        content = (rendered_project / "compose" / "local" / "Dockerfile").read_text()
        assert "uv" in content.lower()


class TestEnvelopeContract:
    def test_common_module_exists(self, rendered_project: Path) -> None:
        common = rendered_project / "src" / "common"
        for filename in (
            "__init__.py",
            "pagination.py",
            "views.py",
            "exceptions.py",
            "spectacular.py",
        ):
            assert (common / filename).exists()

    def test_settings_wire_envelope_stack(self, rendered_project: Path) -> None:
        content = (rendered_project / "config" / "settings" / "base.py").read_text()
        assert "src.common.pagination.EnvelopePageNumberPagination" in content
        assert "src.common.exceptions.envelope_exception_handler" in content
        assert "src.common.spectacular.EnvelopeAutoSchema" in content
        assert "envelope_postprocessing_hook" in content

    def test_users_views_use_envelope_viewset(self, rendered_project: Path) -> None:
        content = (rendered_project / "src" / "users" / "views.py").read_text()
        assert "EnvelopeModelViewSet" in content
        assert 'url_path="all"' in content
        assert "IsAuthenticated" in content


class TestPackaging:
    def test_hatch_packages_explicit(self, rendered_project: Path) -> None:
        content = (rendered_project / "pyproject.toml").read_text()
        assert 'packages = ["config", "src"]' in content

    def test_dockerfiles_do_not_require_uv_lock(self, rendered_project: Path) -> None:
        for compose_dir in ("local", "production"):
            dockerfile = (rendered_project / "compose" / compose_dir / "Dockerfile").read_text()
            assert "uv.lock" not in dockerfile

    def test_schema_urls_use_direct_views(self, rendered_project: Path) -> None:
        content = (rendered_project / "config" / "urls.py").read_text()
        assert "SpectacularAPIView" in content
        assert "drf_spectacular.urls" not in content
