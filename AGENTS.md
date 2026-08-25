# AGENTS.md

This repo is a **cookiecutter template**, not a Django project. There are two layers:

- **Root** (`tests/`, `pyproject.toml`): meta-tests that render the template via
  `cookiecutter --no-input` into a tmp dir and assert on the rendered output.
- **`{{cookiecutter.project_slug}}/`**: the actual Django project template.
  This is a literal Jinja directory name — never rename it. Files inside use
  `{{ cookiecutter.* }}` placeholders; escape literal `{%`/`{{` with `{% raw %}`.
- `hooks/post_gen_project.py`: runs post-generation — injects secret key into
  `.envs/.local`, chmods celery start scripts, deletes `.envs/.production` and
  `.envs/.test`. Those env files exist only in this template, not in generated projects.

## Commands

```bash
# Repo root — verify the template (renders + asserts structure)
uv sync && uv run pytest
```

Commands inside a *generated* project (not this repo) come from its Makefile — see
`{{cookiecutter.project_slug}}/AGENTS.md` for guidance that ships with generated projects.

- Root pytest config differs from the generated project's pytest config (root has no
  pytest-django / DJANGO_SETTINGS_MODULE).

## Template conventions

- New features go in `{{cookiecutter.project_slug}}/`; if structural, mirror with an
  assertion in `tests/test_template.py` (that's how CI verifies the template).
- Generated layout: settings split `config/settings/{base,local,production,test}.py`,
  env via django-environ from `.envs/.env`, apps under `src/` with per-app
  services/selectors/factories/tasks modules, tests co-located in `src/<app>/tests/`.
- Lint/typecheck order in generated-project CI: ruff check → ruff format --check → mypy → pytest.

## API response envelope (binding contract for all DRF endpoints)

Every response is wrapped:

    success     : boolean
    pagination  : object | null   # null when not paginated, never {}
    data        : object | array | null
    errors      : array | null

Paginated responses add
`pagination: {count: int, page_size: int, next: uri|null, previous: uri|null}`.

Implementation rules:

- Build on DRF pagination infrastructure (`get_paginated_response()` etc.); do NOT
  reimplement paging. Extract metadata generically — don't couple the envelope to one
  concrete pagination class. Preferred shape: custom pagination base class +
  drf-spectacular schema extension.
- Detail endpoints (`retrieve`) bypass pagination entirely, so a view-level/mixin envelope
  wrapper is still required alongside the pagination class.
- `page_size` must be the effective page size of THIS response (default, client-provided
  clamped to max). If the pagination class can't expose one meaningfully, fall back to
  `len(data)` rather than omitting/nulling the field.
- drf-spectacular must emit typed schemas: `data` keeps the serializer `$ref`, paginated
  lists get a real Pagination object (count/page_size int, next/previous nullable uri).
  No generic `object` collapse; standard CRUD endpoints must not need manual `@extend_schema`.
- Required tests per pagination scenario (default/client/max page size, first/middle/last
  page, empty queryset, next/previous null combos, non-paginated endpoint): assert all four
  top-level fields. Also add schema tests asserting the Envelope structure distinguishes
  detail (`data: User`) / non-paginated list / paginated list.
