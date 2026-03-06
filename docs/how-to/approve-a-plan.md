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

## Programmatically validating the plan

Instead of manually reviewing plans, you can write automation to fetch the plan from the session's activities and validate the `PlanStep`s against custom business logic.

```python
import time
from jules import JulesClient
from jules.models import ActivityType, Plan

def main() -> None:
    with JulesClient() as client:
        # Create a session requiring plan approval
        session = client.create_session(
            prompt="Refactor the authentication module",
            require_plan_approval=True,
            source="github/davideast/jules-sdk-python"
        )

        print(f"Waiting for plan generation on session: {session.name}...")

        # Poll activities until a plan is generated
        plan_activity = None
        while True:
            activities = client.list_activities(session.name)
            for activity in activities:
                if activity.type.value == ActivityType.PLAN_GENERATED.value:
                    plan_activity = activity
                    break
            if plan_activity:
                break
            time.sleep(2)

        # Parse the plan details
        # The planGenerated details contains the Plan object fields
        plan = Plan.from_dict(plan_activity.details)
        print(f"Found plan with {len(plan.steps)} steps.")

        # Custom validation logic
        forbidden_terms = ["rm -rf", "drop table"]
        plan_rejected = False

        for step in plan.steps:
            description = step.description.lower()
            for term in forbidden_terms:
                if term in description:
                    print(f"Plan step {step.index} '{step.title}' rejected! Contains forbidden term: '{term}'")
                    plan_rejected = True
                    break

        if plan_rejected:
            # Note: The JulesClient currently does not have a reject_plan() method.
            # You might log an error, pause automation, or delete the session.
            print("Plan rejected. Deleting session.")
            client.delete_session(session.name)
        else:
            print("Plan validated successfully. Approving...")
            client.approve_plan(session.name)

if __name__ == "__main__":
    main()
```
