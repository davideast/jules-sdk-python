# Your first session

This tutorial covers the absolute basics of interacting with the Jules API using the Python SDK. We will set up a client, create a session to run a simple prompt, and monitor its progress until it finishes.

## Prerequisites

Before starting, ensure you have your API key set as an environment variable:

```bash
export JULES_API_KEY=your-key
```

## Step 1: Initialize the client

The easiest way to work with the SDK is using `JulesClient` as a context manager. This ensures connections are properly closed when you're done.

Create a new file called `my_session.py`:

```python
from jules import JulesClient

def main() -> None:
    with JulesClient() as client:
        print("Client initialized!")

if __name__ == "__main__":
    main()
```

## Step 2: Configure the source context

Jules needs to know where to operate. In this example, we'll provide a GitHub repository source context.

Add the required imports and configure a `SourceContext` object:

```python
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext

def main() -> None:
    with JulesClient() as client:
        # Configure source to be the requested repository
        source_context = SourceContext(
            source="sources/github/davideast/jules-sdk-python",
            github_repo_context=GitHubRepoContext(
                starting_branch="main"
            )
        )
        print("Source context ready.")

if __name__ == "__main__":
    main()
```

## Step 3: Create the session

Now we submit a task to Jules by creating a session with our prompt and the `source_context`:

```python
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext

def main() -> None:
    with JulesClient() as client:
        source_context = SourceContext(
            source="sources/github/davideast/jules-sdk-python",
            github_repo_context=GitHubRepoContext(
                starting_branch="main"
            )
        )

        print("Creating a new Jules session...")
        session = client.create_session(
            prompt="Write a hello world program in Python",
            source_context=source_context
        )
        print(f"Session created: {session.name} (State: {session.state.value})")

if __name__ == "__main__":
    main()
```

## Step 4: Monitor the progress

Jules processes tasks asynchronously. To find out when the task is done, we need to poll the session state.

We will use the `SessionState` enum to check if the session has reached a terminal state (such as `COMPLETED`, `FAILED`, or `CANCELLED`).

```python
import time
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext, SessionState

def main() -> None:
    with JulesClient() as client:
        source_context = SourceContext(
            source="sources/github/davideast/jules-sdk-python",
            github_repo_context=GitHubRepoContext(
                starting_branch="main"
            )
        )

        session = client.create_session(
            prompt="Write a hello world program in Python",
            source_context=source_context
        )
        print(f"Session created: {session.name}")

        print("Polling session state until completed or failed...")
        while True:
            current_session = client.get_session(session.name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session finished with state: {current_session.state.value}")
                break

            time.sleep(2)

        print("Cleaning up session...")
        client.delete_session(session.name)
        print("Session deleted.")

if __name__ == "__main__":
    main()
```

## Running the code

Run your script:

```bash
python my_session.py
```

You should see output similar to:
```
Creating a new Jules session...
Session created: sessions/12345 (State: QUEUED)
Polling session state until completed or failed...
Current state: RUNNING
Current state: IN_PROGRESS
Current state: COMPLETED
Session finished with state: COMPLETED
Cleaning up session...
Session deleted.
```

You've now successfully created and completed your first Jules session!
