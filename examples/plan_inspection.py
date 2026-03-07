"""Retrieving and inspecting a session plan before approval using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/plan_inspection.py
"""
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        print("Fetching a session awaiting plan approval...")
        sessions = list(client.list_sessions())

        # Safely check for AWAITING_PLAN_APPROVAL state, working around missing Enum values
        target_state = getattr(SessionState, "AWAITING_PLAN_APPROVAL", "AWAITING_PLAN_APPROVAL")
        awaiting_sessions = [s for s in sessions if getattr(s.state, "value", str(s.state)) == target_state]

        if not awaiting_sessions:
            print("No sessions awaiting plan approval. Try creating one with `require_plan_approval=True`.")
            return

        session = awaiting_sessions[0]
        print(f"Inspecting plan for session: {session.name}")

        # Fetch the plan directly using the client.plan() method
        plan = client.plan(session.name)
        if not plan:
            print("No plan found for this session.")
            return

        print("\nProposed Plan Steps:")
        for step in plan.steps:
            print(f"{step.index}. {step.title}")
            print(f"   -> {step.description}")

        print("\nNote: Call `client.approve_plan(session.name)` when satisfied.")

if __name__ == "__main__":
    main()
