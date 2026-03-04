# How to approve a plan

By default, Jules may automatically execute a plan generated for your session without asking for your approval. You can explicitly require manual approval before Jules begins execution, allowing you to review the plan steps first.

This guide shows you how to pause a session after plan generation and approve it.

## Create a session requiring approval

To require a plan review, pass `require_plan_approval=True` to `create_session()`. The session will pause in the `AWAITING_PLAN_APPROVAL` state once the plan is generated.

```python
from jules import JulesClient

def main() -> None:
    with JulesClient() as client:
        print("Creating session requiring plan approval...")
        session = client.create_session(
            prompt="Refactor the authentication module",
            require_plan_approval=True,
            source="github/davideast/jules-sdk-python"
        )
        print(f"Session created: {session.name}")

if __name__ == "__main__":
    main()
```

## Approve the plan

To resume execution once you're satisfied with the plan, you must approve the plan by calling `approve_plan(session_name)`. The session will resume and enter the `IN_PROGRESS` state.

```python
from jules import JulesClient

def main() -> None:
    with JulesClient() as client:
        # Create a session requiring plan approval
        session = client.create_session(
            prompt="Refactor the authentication module",
            require_plan_approval=True,
            source="github/davideast/jules-sdk-python"
        )

        # Approve the plan
        print("Simulating plan review... approving plan.")
        try:
            client.approve_plan(session.name)
            print("Plan approved successfully.")
        except Exception as e:
            print(f"Failed to approve plan or plan not ready: {e}")

        print("Cleaning up...")
        client.delete_session(session.name)
        print("Done.")

if __name__ == "__main__":
    main()
```

For more details on session methods, see the [`JulesClient` Reference](../reference/client.md).
