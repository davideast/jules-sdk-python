"""Creating sessions that automatically generate pull requests.

Usage:
    export JULES_API_KEY=your-key
    python examples/automation_workflow.py
"""
import time
from jules import JulesClient
from jules.models import AutomationMode, SessionState

def main() -> None:
    with JulesClient() as client:
        print("Creating a session configured to auto-create a pull request...")

        # Using AUTO_CREATE_PR tells the agent to open a PR on completion
        session = client.create_session(
            prompt="Fix formatting issues in the README",
            automation_mode=AutomationMode.AUTO_CREATE_PR
        )
        print(f"Session created: {session.name}")
        print(f"Automation Mode: {session.automation_mode.value}")

        print("\nNote: When this session reaches COMPLETED state,")
        print("it will contain a PullRequest in its outputs.")

        print("\nCleaning up...")
        client.delete_session(session.name)
        print("Done.")

if __name__ == "__main__":
    main()
