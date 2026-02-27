# jules-sdk-python

Idiomatic Python SDK for the Jules API.

## Installation

```bash
pip install jules-sdk
```

## Usage

```python
from jules import JulesClient

with JulesClient() as client:
    # list sessions
    for session in client.list_sessions():
        print(session.name)

    # create a session
    session = client.create_session("Refactor the login module")
    print(f"Created session: {session.name}")
```

## Development

See `Makefile` for common tasks:
- `make test`: Run tests
- `make lint`: Run type checks
