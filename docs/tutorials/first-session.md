# Your first session

This tutorial covers the absolute basics of interacting with the Jules API using the Python SDK. We will set up a client, create a session to run a simple prompt, monitor its progress until it generates a plan, review and approve the plan, and finally inspect the resulting codebase changes.

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
        print("Source context ready.")

if __name__ == "__main__":
    main()
```

## Step 3: Create the session

Now we submit a task to Jules by creating a session. To ensure we have full control over what Jules does, we will set `require_plan_approval=True`. This tells Jules to pause and wait for our permission before executing its plan.

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
            source_context=source_context,
            require_plan_approval=True
        )
        print(f"Session created: {session.name} (State: {session.state.value})")

if __name__ == "__main__":
    main()
```

## Step 4: Monitor for the plan

Jules processes tasks asynchronously. Because we required plan approval, we need to poll the session state until it reaches the `AWAITING_USER_FEEDBACK` state.

```python
import time
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext, SessionState

def main() -> None:
    with JulesClient() as client:
        # ... setup and session creation ...
        session = client.create_session(
            prompt="Write a hello world program in Python",
            source_context=SourceContext(source="sources/github/davideast/jules-sdk-python", github_repo_context=GitHubRepoContext(starting_branch="main")),
            require_plan_approval=True
        )

        print("Polling session state until it awaits feedback...")
        while True:
            current_session = client.get_session(session.name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state == SessionState.AWAITING_USER_FEEDBACK:
                print("Session is paused, awaiting plan approval.")
                break
            elif current_session.state in (SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session failed or cancelled early: {current_session.state.value}")
                return

            time.sleep(2)

if __name__ == "__main__":
    main()
```

## Step 5: Review the plan

When the session is in the `AWAITING_USER_FEEDBACK` state, we can inspect the generated plan by fetching the session's activities and looking for the `PLAN_GENERATED` activity.

```python
import time
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext, SessionState, ActivityType, Plan

def main() -> None:
    with JulesClient() as client:
        # ... session creation and polling ...
        session = client.get_session("sessions/123") # Assuming we reached AWAITING_USER_FEEDBACK

        # Fetch activities to find the plan
        activities = list(client.list_activities(session.name))
        plan_activity = next((a for a in activities if a.type == ActivityType.PLAN_GENERATED), None)

        if plan_activity and 'plan' in plan_activity.details:
            plan = Plan.from_dict(plan_activity.details['plan'])
            print(f"Plan generated on {plan.create_time}:")
            for step in plan.steps:
                print(f" - Step {step.index + 1}: {step.title}")
                print(f"   {step.description}")

if __name__ == "__main__":
    main()
```

## Step 6: Approve the plan and wait for completion

Once you have reviewed the plan, you can approve it to allow the session to continue executing. We then poll again until the session reaches a terminal state.

```python
import time
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        # ... setup, creation, review ...
        session_name = "sessions/123"

        # Approve the plan
        print("Approving the plan...")
        client.approve_plan(session_name)

        # Poll again until completion
        print("Polling session state until completed or failed...")
        while True:
            current_session = client.get_session(session_name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session finished with state: {current_session.state.value}")
                break

            time.sleep(2)

if __name__ == "__main__":
    main()
```

## Step 7: Inspect the output

When the session is complete, it provides a `ChangeSet` containing the actual git patch and suggested commit message.

```python
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        # ... completion polling ...
        current_session = client.get_session("sessions/123")

        if current_session.state == SessionState.COMPLETED:
            for output in current_session.outputs:
                if output.change_set:
                    patch = output.change_set.git_patch
                    print("Session completed successfully. Review the changes:")
                    print(f"Suggested commit message: {patch.suggested_commit_message}")
                    print(f"Patch:\n{patch.unidiff_patch}")

if __name__ == "__main__":
    main()
```

## Putting it all together

Here is the complete, runnable script combining all the steps:

```python
import time
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext, SessionState, ActivityType, Plan

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
            source_context=source_context,
            require_plan_approval=True
        )
        print(f"Session created: {session.name}")

        print("Polling session state until it awaits feedback...")
        while True:
            current_session = client.get_session(session.name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state == SessionState.AWAITING_USER_FEEDBACK:
                print("Session is paused, awaiting plan approval.")
                break
            elif current_session.state in (SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session failed or cancelled early: {current_session.state.value}")
                return

            time.sleep(2)

        # Review the plan
        activities = list(client.list_activities(session.name))
        plan_activity = next((a for a in activities if a.type == ActivityType.PLAN_GENERATED), None)

        if plan_activity and 'plan' in plan_activity.details:
            plan = Plan.from_dict(plan_activity.details['plan'])
            print(f"Plan generated on {plan.create_time}:")
            for step in plan.steps:
                print(f" - Step {step.index + 1}: {step.title}")
                print(f"   {step.description}")

        # Approve the plan
        print("Approving the plan...")
        client.approve_plan(session.name)

        # Poll again until completion
        print("Polling session state until completed or failed...")
        while True:
            current_session = client.get_session(session.name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session finished with state: {current_session.state.value}")
                break

            time.sleep(2)

        # Inspect the output
        if current_session.state == SessionState.COMPLETED:
            for output in current_session.outputs:
                if output.change_set:
                    patch = output.change_set.git_patch
                    print("Session completed successfully. Review the changes:")
                    print(f"Suggested commit message: {patch.suggested_commit_message}")
                    print(f"Patch:\n{patch.unidiff_patch}")

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
Session created: sessions/12345
Polling session state until it awaits feedback...
Current state: RUNNING
Current state: PLANNING
Current state: AWAITING_USER_FEEDBACK
Session is paused, awaiting plan approval.
Plan generated on 2023-10-27T10:00:00Z:
 - Step 1: Create hello_world.py
   Write a basic hello world script.
Approving the plan...
Polling session state until completed or failed...
Current state: IN_PROGRESS
Current state: COMPLETED
Session finished with state: COMPLETED
Session completed successfully. Review the changes:
Suggested commit message: Add hello_world.py
Patch:
--- /dev/null
+++ b/hello_world.py
@@ -0,0 +1,2 @@
+print("Hello, world!")
Cleaning up session...
Session deleted.
```

You've now successfully created and completed your first Jules session, reviewed the execution plan, and inspected the generated changes!
