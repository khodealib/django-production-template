.PHONY: help up down migrate seed test test-cov lint lint-fix format typecheck shell dbshell install pre-commit

MANAGE = uv run python manage.py

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

up: ## Start local development stack
	docker compose -f compose/local/docker-compose.yml up

down: ## Stop local development stack
	docker compose -f compose/local/docker-compose.yml down

logs: ## View logs from local stack
	docker compose -f compose/local/docker-compose.yml logs -f

migrate: ## Run database migrations
	$(MANAGE) migrate

makemigrations: ## Create new migrations
	$(MANAGE) makemigrations

seed: ## Seed database with sample data
	$(MANAGE) seed_data

createsuperuser: ## Create a superuser
	$(MANAGE) createsuperuser

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov --cov-report=term-missing

lint: ## Run linter
	uv run ruff check .

lint-fix: ## Run linter with auto-fix
	uv run ruff check --fix .

format: ## Format code
	uv run ruff format .

typecheck: ## Run type checker
	uv run mypy .

shell: ## Open Django shell
	$(MANAGE) shell_plus || $(MANAGE) shell

dbshell: ## Open database shell
	$(MANAGE) dbshell

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

collectstatic: ## Collect static files
	$(MANAGE) collectstatic --noinput
