"""Retrieving and inspecting a session plan before approval using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/plan_inspection.py
"""
from jules import JulesClient
from jules.models import SessionState, ActivityType

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

        # Find the activity that contains the generated plan
        activities = list(client.list_activities(session.name))
        plan_activity = next((a for a in activities if getattr(a.type, "value", str(a.type)) == "planGenerated"), None)

        if not plan_activity or "plan" not in plan_activity.details:
            print("No plan details found in activities.")
            return

        plan_data = plan_activity.details["plan"]
        print("\nProposed Plan Steps:")
        for step in plan_data.get("steps", []):
            print(f"{step['index']}. {step['title']}")
            print(f"   -> {step['description']}")

        print("\nNote: Call `client.approve_plan(session.name)` when satisfied.")

if __name__ == "__main__":
    main()
