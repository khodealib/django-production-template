# AGENTS.md

Guidance for AI agents working inside this Django project.

## Commands

Use Makefile targets — never raw `python manage.py` (manage.py lives at the project root):

```bash
make install     # uv sync
make up / down   # Docker dev stack (postgres, redis, web, celery)
make migrate / makemigrations / seed / createsuperuser
make test        # pytest; make test-cov for coverage
make lint        # ruff check
make lint-fix / format
make typecheck   # mypy
make shell / dbshell
make pre-commit  # pre-commit run --all-files
```

CI order: ruff check → ruff format --check → mypy → pytest.

## Layout

- Settings split: `config/settings/{base,local,production,test}.py`. Env via django-environ
  from `.envs/.env`.
- Apps live under `src/<app>/` with per-app `services.py`, `selectors.py`, `factories.py`,
  `tasks.py`; tests co-located in `src/<app>/tests/`.
- Custom user model: `users.User` (`AUTH_USER_MODEL`). Never use `auth.User`.
- pytest markers: `slow`, `integration` (deselect with `-m "not slow"`).

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
