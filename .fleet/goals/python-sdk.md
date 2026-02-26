# Build a Python REST Client for the Jules API

Create an idiomatic Python SDK (`jules-sdk`) wrapping the Jules REST API. The SDK should feel native to Python — `dataclasses`, `httpx`, iterator-based pagination, context managers. Target Python 3.10+, under 1000 lines of source.

## Tools
- API Discovery Doc: `curl -s https://jules.googleapis.com/\$discovery/rest?version=v1alpha`
- Validate packaging: `python -m build --sdist`
- Run tests: `python -m pytest tests/ -v`
- Type check: `python -m mypy src/jules/`

## Assessment Hints

Assessments should be scoped as independent, mergeable PRs. Create one assessment per phase:

- **Project scaffolding** — `pyproject.toml` (name `jules-sdk`, deps `httpx>=0.27`), `src/jules/` package with `__init__.py` and `py.typed`, `tests/` dir, [README.md](file:///Users/deast/google-labs-code/jules-sdk/packages/fleet/README.md) with usage example, `Makefile` with `test`/`lint`/`typecheck` targets
- **Data models** — `src/jules/models.py` with `dataclasses` for [Session](file:///Users/deast/google-labs-code/jules-sdk/packages/core/src/types.ts#162-196), `Activity`, `Plan`, `PlanStep`, [Source](file:///Users/deast/google-labs-code/jules-sdk/packages/core/src/types.ts#249-262), [GitHubRepo](file:///Users/deast/google-labs-code/jules-sdk/packages/core/src/types.ts#229-236), `SessionOutput`, [PullRequest](file:///Users/deast/google-labs-code/jules-sdk/packages/core/src/types.ts#270-277). Python `enum.Enum` for `SessionState`, `AutomationMode`, `ActivityType`. Each model needs `from_dict(cls, data)` and `to_dict(self)` classmethods. Derive all types from the discovery doc.
- **Client** — `src/jules/client.py` with `JulesClient` using `httpx.Client`. API key via `x-goog-api-key` header, `JULES_API_KEY` env fallback. Context manager support (`with JulesClient(...) as client:`). Methods: `sessions.create()`, `.get()`, `.list()` (returns `Iterator[Session]` via `__iter__` pagination), `.delete()`, `.send_message()`, `.activities()`, `.plan()`, `.approve_plan()`, `sources.list()`. Typed `JulesAPIError` exceptions.
- **Test suite** — `pytest` + `respx` (httpx mock). Cover: session CRUD, pagination, error handling, model roundtrip serialization.

Keep the README accurate as the API surface evolves — usage examples should reflect the actual client interface.

## Insight Hints
- Report on total API surface (methods × resources) from the discovery doc
- Note any API methods that don't map cleanly to Python patterns
- Note if the discovery doc schema has changed since this goal was written

## Constraints
- This is a standalone Python project — build it independently from scratch
- Use `dataclasses` (zero runtime deps beyond httpx)
- Use `httpx` for HTTP
- Follow the Red-Green-Refactor (traffic light) approach: write a failing test first (red), implement until it passes (green), then clean up (refactor)
- Keep each assessment to one logical layer (models, client, tests)
- Every file must have a module docstring and full type annotations
- Cross-reference existing milestone issues before creating new ones to avoid duplicates

