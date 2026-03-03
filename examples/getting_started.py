"""Getting started with the Jules SDK: Creating and monitoring a session.

Usage:
    export JULES_API_KEY=your-key
    python examples/getting_started.py
"""
import time
from jules import JulesClient
from jules.models import SessionState
from jules.models import SourceContext, GitHubRepoContext, GitHubRepo, GitHubBranch

def main() -> None:
    with JulesClient() as client:
        print("Creating a new Jules session...")

        # Configure source to be the requested repository
        source_context = SourceContext(
            source="sources/github/davideast/jules-sdk-python",
            github_repo_context=GitHubRepoContext(
                starting_branch="main"
            )
        )

        # We also need to add the sourceContext parameter to create_session
        session = client.create_session(
            prompt="Write a hello world program in Python",
            source_context=source_context
        )
        print(f"Session created: {session.name} (State: {session.state.value})")

        print("Polling session state until completed or failed...")
        while True:
            current_session = client.get_session(session.name)
            print(f"Current state: {current_session.state.value}")

            if current_session.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
                print(f"Session finished with state: {current_session.state.value}")
                break

            time.sleep(2)

        print("Cleaning up session...")
        client.delete_session(session.name)
        print("Session deleted.")

if __name__ == "__main__":
    main()