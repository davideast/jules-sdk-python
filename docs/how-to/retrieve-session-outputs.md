# How to retrieve session outputs

When a Jules session completes successfully, it may produce outputs depending on its task and configuration. This guide shows how to retrieve code patches (ChangeSets) and pull request links from a session.

## Understanding session outputs

Session results are stored in the `outputs` list on the `Session` object. Each item is a `SessionOutput` which can contain:

*   **`change_set`**: If Jules wrote code or modified files, the output includes a `ChangeSet` containing a unified diff (`git_patch.unidiff_patch`).
*   **`pull_request`**: If Jules was configured with `AutomationMode.AUTO_CREATE_PR` or explicitly created a PR, the output includes a `PullRequest` containing the GitHub URL and details.

Because a single session can theoretically produce multiple outputs, you must iterate through the `outputs` list.

## Retrieving a code patch

To get the raw code changes proposed by Jules, extract the unified diff from the `ChangeSet`.

```python
from jules import JulesClient
from jules.models import SessionState

def print_session_patches(client: JulesClient, session_name: str) -> None:
    session = client.get_session(session_name)

    if session.state != SessionState.COMPLETED:
        print(f"Session is not complete. Current state: {session.state.value}")
        return

    for output in session.outputs:
        if output.change_set:
            patch = output.change_set.git_patch.unidiff_patch
            print(f"--- Patch for source: {output.change_set.source} ---")
            print(patch)

if __name__ == "__main__":
    with JulesClient() as client:
        # Assuming you have a completed session name
        session_name = "sessions/12345"
        print_session_patches(client, session_name)
```

## Retrieving a pull request URL

When using `AutomationMode.AUTO_CREATE_PR`, Jules automatically pushes the code to a branch and opens a PR. You can extract the link to this PR from the `PullRequest` output.

```python
from jules import JulesClient
from jules.models import AutomationMode

def create_and_get_pr(client: JulesClient, source_repo: str) -> None:
    # 1. Create a session that automatically opens a PR
    session = client.create_session(
        prompt="Fix the typo in README.md",
        source=source_repo,
        automation_mode=AutomationMode.AUTO_CREATE_PR
    )
    print(f"Started session: {session.name}")

    # 2. Wait for it to complete (simplified for this example)
    import time
    from jules.models import SessionState

    while True:
        session = client.get_session(session.name)
        if session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
            break
        time.sleep(5)

    if session.state != SessionState.COMPLETED:
        print("Session did not complete successfully.")
        return

    # 3. Extract the PR URL
    found_pr = False
    for output in session.outputs:
        if output.pull_request:
            print(f"Success! PR created at: {output.pull_request.url}")
            found_pr = True

    if not found_pr:
        print("Session completed but no PR was found in outputs.")

if __name__ == "__main__":
    with JulesClient() as client:
        # Replace with your target repository
        create_and_get_pr(client, "sources/github/owner/repo")
```

For more details on the models involved, see the [Models reference](../reference/models.md).
