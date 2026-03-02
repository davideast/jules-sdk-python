"""Interactive plan review workflow using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/plan_review.py
"""
import time
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        print("Creating session requiring plan approval...")
        session = client.create_session(
            prompt="Refactor the authentication module",
            require_plan_approval=True,
            source="github/davideast/jules-sdk-python"
        )
        print(f"Session created: {session.name}")

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
