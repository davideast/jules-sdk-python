# jules-sdk-python

Idiomatic Python SDK for the Jules API.

## Installation

```bash
pip install jules-sdk
```

## Quickstart

```python
from jules import JulesClient

with JulesClient() as client:
    session = client.create_session("Refactor the login module", source="github/owner/repo")
    print(f"Created session: {session.name}")
```

## Documentation

**Learning Jules**
- [Your first session](docs/tutorials/first-session.md) — start here

**Doing things**
- [Wait for a session to finish](docs/how-to/poll-to-completion.md)
- [Approve a plan](docs/how-to/approve-a-plan.md)
- [Handle errors](docs/how-to/handle-errors.md)
- [Attach sources](docs/how-to/attach-sources.md)

**Looking things up**
- [JulesClient](docs/reference/client.md)
- [Models](docs/reference/models.md)
- [Errors](docs/reference/errors.md)
- [Session states](docs/reference/session-states.md)

**Understanding Jules**
- [How sessions work](docs/explanation/sessions.md)
- [How sources work](docs/explanation/sources.md)
- [Architecture and design](docs/explanation/architecture.md)

## Development

See `Makefile` for common tasks:
- `make test`: Run tests
- `make lint`: Run type checks