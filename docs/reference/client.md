# JulesClient

The `JulesClient` is the main entry point to interacting with the Jules API.

### `JulesClient(api_key: Optional[str] = None, base_url: str = "https://jules.googleapis.com/v1alpha")`

Initializes the API client. If `api_key` is not provided, it looks for the `JULES_API_KEY` environment variable.

The client acts as a context manager and can be used with `with` statements.

```python
from jules import JulesClient

with JulesClient() as client:
    pass
```

### Methods

#### `create_session(prompt: str, require_plan_approval: Optional[bool] = None, source: Optional[str] = None, source_context: Optional[SourceContext] = None) -> Session`

Creates a new Jules session.
*   **`prompt`** (`str`): The primary task description defining what the AI agent should accomplish.
*   **`require_plan_approval`** (`bool`, optional): If `True`, the session will pause in `AWAITING_PLAN_APPROVAL` once a plan is generated. Defaults to `None` (auto-approve).
*   **`source`** (`str`, optional): A convenient shorthand identifier for the environment context, formatted as `sources/github/{owner}/{repo}`.
*   **`source_context`** (`SourceContext`, optional): A deeply configured object representing the context in which the session operates. Mutually exclusive with `source`.
*   **Returns** (`Session`): An instantiated `Session` model reflecting the created resource, usually starting in `STATE_UNSPECIFIED` or `QUEUED`.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 400 for invalid prompts, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures (e.g., connection resets) via `httpx.RequestError`.

#### `get_session(name: str) -> Session`

Gets the details of an existing session.
*   **`name`** (`str`): The unique name/identifier of the session.
*   **Returns** (`Session`): A `Session` object populated with current state and information.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if the session doesn't exist, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `list_sessions() -> Iterator[Session]`

Lists all active and past sessions for your account using pagination.
*   **Returns** (`Iterator[Session]`): An iterator yielding `Session` objects sequentially.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `delete_session(name: str) -> None`

Deletes a session entirely.
*   **`name`** (`str`): The unique name/identifier of the session to delete.
*   **Returns** (`None`):
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if the session doesn't exist, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `send_message(session_name: str, message: str) -> None`

Sends a message prompt to a running session.
*   **`session_name`** (`str`): The unique name/identifier of the session.
*   **`message`** (`str`): The prompt/message to send to the session.
*   **Returns** (`None`):
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 400 for invalid prompts, 404 if the session is not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `get_activity(name: str) -> Activity`

Gets the details of a session activity.
*   **`name`** (`str`): The unique name/identifier of the activity.
*   **Returns** (`Activity`): An `Activity` object describing the event.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if the activity is not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `list_activities(session_name: str) -> Iterator[Activity]`

Lists all activities within a session using pagination.
*   **`session_name`** (`str`): The unique name/identifier of the session whose activities to list.
*   **Returns** (`Iterator[Activity]`): An iterator yielding `Activity` objects sequentially.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if the session is not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `approve_plan(name: str) -> None`

Approves a plan, resuming session execution.
*   **`name`** (`str`): The unique name/identifier of the session waiting for plan approval.
*   **Returns** (`None`):
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 400 if the session is not waiting for a plan approval, 404 if not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `archive_session(name: str) -> None`

Archives a session.
*   **`name`** (`str`): The unique name/identifier of the session to archive.
*   **Returns** (`None`):
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `unarchive_session(name: str) -> None`

Unarchives a previously archived session.
*   **`name`** (`str`): The unique name/identifier of the session to unarchive.
*   **Returns** (`None`):
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `get_source(name: str) -> Source`

Gets detailed information about a source repository.
*   **`name`** (`str`): The unique name/identifier of the source.
*   **Returns** (`Source`): A `Source` object detailing the repository.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 404 if the source is not found, or 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.

#### `list_sources() -> Iterator[Source]`

Lists all available source repositories in your account using pagination.
*   **Returns** (`Iterator[Source]`): An iterator yielding `Source` objects sequentially.
*   **Raises**:
    *   `JulesAPIError`: Raised with status code 401 for bad authentication.
    *   `JulesError`: Raised for underlying network failures via `httpx.RequestError`.
