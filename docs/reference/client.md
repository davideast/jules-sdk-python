# JulesClient

The `JulesClient` is the main entry point to interacting with the Jules API.

### `JulesClient(api_key=None, base_url="https://jules.googleapis.com/v1alpha")`

Initializes the API client. If `api_key` is not provided, it looks for the `JULES_API_KEY` environment variable.

The client acts as a context manager and can be used with `with` statements.

```python
from jules import JulesClient

with JulesClient() as client:
    pass
```

### Methods

#### `create_session(prompt: str, require_plan_approval: Optional[bool] = None, source: Optional[str] = None, source_context: Optional[Any] = None) -> Session`

Creates a new Jules session.
*   **`prompt`**: The task description.
*   **`require_plan_approval`**: Optional boolean requiring explicit plan approval.
*   **`source`**: Optional shorthand source string (e.g. `github/owner/repo`).
*   **`source_context`**: Optional `SourceContext` object to attach a repository.
*   **Returns**: A `Session` object.
*   **Raises**: `JulesAPIError` or `JulesError` on failure.

#### `get_session(name: str) -> Session`

Gets the details of an existing session.
*   **`name`**: The name of the session.
*   **Returns**: A `Session` object.

#### `list_sessions() -> Iterator[Session]`

Lists all active and past sessions for your account.
*   **Returns**: An iterator yielding `Session` objects.

#### `delete_session(name: str) -> None`

Deletes a session entirely.
*   **`name`**: The name of the session.

#### `send_message(session_name: str, message: str) -> None`

Sends a message prompt to a running session.
*   **`session_name`**: The name of the session.
*   **`message`**: The prompt to send.

#### `get_activity(name: str) -> Activity`

Gets the details of a session activity.
*   **`name`**: The name of the activity.
*   **Returns**: An `Activity` object.

#### `list_activities(session_name: str) -> Iterator[Activity]`

Lists all activities within a session.
*   **`session_name`**: The name of the session.
*   **Returns**: An iterator yielding `Activity` objects.

#### `approve_plan(name: str) -> None`

Approves a plan, resuming session execution.
*   **`name`**: The name of the session.

#### `archive_session(name: str) -> None`

Archives a session.
*   **`name`**: The name of the session.

#### `unarchive_session(name: str) -> None`

Unarchives a previously archived session.
*   **`name`**: The name of the session.

#### `get_source(name: str) -> Source`

Gets detailed information about a source repository.
*   **`name`**: The name of the source.
*   **Returns**: A `Source` object.

#### `list_sources() -> Iterator[Source]`

Lists all available source repositories in your account.
*   **Returns**: An iterator yielding `Source` objects.
