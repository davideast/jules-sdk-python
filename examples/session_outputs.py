"""Retrieving outputs from a completed session using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/session_outputs.py
"""
import time
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        print("Fetching a recently completed session...")
        # In a real app, this would likely be the session you just polled
        sessions = list(client.list_sessions())
        completed_sessions = [s for s in sessions if s.state == SessionState.COMPLETED]

        if not completed_sessions:
            print("No completed sessions found to inspect outputs.")
            return

        session = completed_sessions[0]
        print(f"Inspecting outputs for session: {session.name}")

        if not session.outputs:
            print("This session completed but returned no outputs.")
        else:
            for idx, output in enumerate(session.outputs):
                print(f"\nOutput #{idx + 1}:")
                if output.pull_request:
                    print(f"  Pull Request URL: {output.pull_request.url}")
                    print(f"  Title: {output.pull_request.title}")
                elif output.change_set:
                    print(f"  Git Patch Generated: Yes")
                    print(f"  Suggested Commit: {output.change_set.git_patch.suggested_commit_message}")

if __name__ == "__main__":
    main()
