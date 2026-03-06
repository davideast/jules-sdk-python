# How to wait for a session to finish

When you create a Jules session, execution happens asynchronously in the background. To know when the session finishes, you must poll its state until it reaches a terminal state.

This guide shows how to wait for a session to finish using a loop and `time.sleep()`.

## Polling a session

The `JulesClient` allows you to retrieve the current state of a session by name. A session reaches a terminal condition when its `state` matches one of the following `SessionState` values:

* `SessionState.COMPLETED`: The session finished successfully.
* `SessionState.FAILED`: The session encountered a fatal error.
* `SessionState.CANCELLED`: The session was manually cancelled or aborted.

You can set up a polling loop to check the session status periodically.

```python
import time
from jules import JulesClient
from jules.models import SessionState

def poll_session(client: JulesClient, session_name: str) -> None:
    print(f"Polling session state until completed or failed...")

    while True:
        current_session = client.get_session(session_name)
        print(f"Current state: {current_session.state.value}")

        if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
            print(f"Session finished with state: {current_session.state.value}")
            break

        # Wait before checking again to avoid rate limits
        time.sleep(2)

if __name__ == "__main__":
    with JulesClient() as client:
        session = client.create_session("Do a simple task")
        poll_session(client, session.name)
```

## Adding a timeout mechanism

While polling, it's a good practice to include a timeout. If the session takes longer than the maximum duration, you should exit the loop to avoid an infinite wait.

```python
import time
from jules import JulesClient
from jules.models import SessionState

def poll_with_timeout(client: JulesClient, session_name: str, max_duration: int = 60) -> None:
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_duration:
            print("Timed out waiting for session to finish.")
            break

        current_session = client.get_session(session_name)
        if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
            print(f"Session finished with state: {current_session.state.value}")
            break

        time.sleep(2)

if __name__ == "__main__":
    with JulesClient() as client:
        session = client.create_session("Do a simple task")
        poll_with_timeout(client, session.name, max_duration=30)
```

See [Session states](../reference/session-states.md) for more details on all available `SessionState` lifecycle values.
