---
milestone: "2"
---
# Use-Case Code Snippets

Create runnable Python code snippets that demonstrate the Jules SDK from a user's perspective. Each snippet tells a short story — a developer trying to accomplish something real. Snippets live in `examples/` as standalone `.py` files.

## Diagnostics
- Existing snippets: `find examples/ -name "*.py" -exec head -5 {} +`
- Run all snippets (dry-run with mocks): `python -m pytest examples/ -v --tb=short`
- Type check snippets: `python -m mypy examples/ --strict`

## Tools
- API Discovery Doc: `curl -s https://jules.googleapis.com/$discovery/rest?version=v1alpha`
- SDK source: `cat src/jules/client.py`
- SDK models: `cat src/jules/models.py`
- README: `cat README.md`

## Assessment Hints

Start by analyzing the SDK source (`src/jules/client.py`, `src/jules/models.py`) and any existing snippets in `examples/`. Identify the distinct **user journeys** the API enables — not just individual methods, but the multi-step workflows a developer would actually follow in practice.

Each assessment creates one snippet file covering a distinct user journey. Organize by scenario, not by API method. Each snippet should:

- Start with a module docstring describing **what the user is trying to accomplish**
- Include realistic variable names and print statements that show what a developer would care about
- Handle errors that a real user would encounter
- End with a clear outcome the user can verify

Here are a few starting points for inspiration, but prioritize what you discover through analysis — the SDK may support compelling workflows beyond these:

- **Getting started** — Initialize a client, create a session, check its state, and clean up. The first thing a new user copies.
- **Watching a session** — Poll a session until it completes, printing progress along the way.
- **Interactive plan review** — Create a session that requires plan approval, inspect the plan steps, then approve.
- **Error recovery** — Handle `JulesAPIError` for common scenarios like invalid keys or missing sessions.

Before creating a new snippet, review the existing files in `examples/` to ensure the use case is genuinely distinct from what already exists. Two snippets may use the same API method if they serve different user stories.

## Snippet Structure

Each snippet file should follow this pattern:

```python
"""<What the user is trying to accomplish>.

Usage:
    export JULES_API_KEY=your-key
    python examples/<filename>.py
"""
from jules import JulesClient

def main():
    with JulesClient() as client:
        # ... use-case-specific code
        pass

if __name__ == "__main__":
    main()
```

Keep snippets under 80 lines. Prefer clarity over cleverness — a new Python developer should understand every line.

## Insight Hints
- Report which SDK methods are covered by at least one snippet and which are uncovered
- Note any API features from the discovery doc that would make compelling use cases but aren't represented yet

## Verification

Each snippet should create its own sessions and clean up after itself — read-only snippets (listing, sources) naturally work against existing state.

Run each snippet against the live API:
- `JULES_API_KEY=$JULES_API_KEY python examples/getting_started.py`
- `JULES_API_KEY=$JULES_API_KEY python examples/list_and_filter.py`
- `JULES_API_KEY=$JULES_API_KEY python examples/sources.py`

Each snippet should run to completion without errors and produce meaningful output to stdout.

### When something goes wrong

If a snippet fails, determine whether the issue is in the snippet or in the SDK:

- **Snippet bug** (e.g. wrong method name, missing import, bad argument) — fix the snippet and re-run.
- **SDK bug** (e.g. a field returns `None` when the API populates it, an endpoint returns an unexpected status code, or `from_dict` crashes on valid API data) — write a detailed report to a temporary file, then file it:
  ```bash
  cat > /tmp/bug-report.md << 'EOF'
  ## Steps to Reproduce
  The snippet file and the exact command used to run it.

  ## Expected Behavior
  What should have happened.

  ## Actual Behavior
  What actually happened, including the full traceback.

  ## Environment
  - Python version: (output of python --version)
  - SDK version: (installed jules-sdk version)
  - OS: (platform)

  ## Additional Context
  Any other observations — response payloads, state of the session, related API quirks.
  EOF

  npx @google/jules-fleet signal create \
    --repo davideast/jules-sdk-python \
    --title "concise bug title" \
    --body-file /tmp/bug-report.md
  ```

  Before filing, review the report for any sensitive information — redact API keys, tokens, or credentials that may appear in tracebacks or HTTP logs. Include any context you believe is critical to diagnosing the issue beyond the fields above.

## Constraints
- Each snippet must be a self-contained, runnable `.py` file
- Use only the public SDK API (`from jules import ...`)
- Include type annotations on all function signatures
- Each file must include a module docstring with a Usage section
- Cross-reference existing snippets in `examples/` before creating new ones — each file should serve a unique user story
