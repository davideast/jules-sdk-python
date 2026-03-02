"""Listing and filtering paginated resources using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/list_and_filter.py
"""
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    with JulesClient() as client:
        print("Fetching sources available in your account...")
        sources = list(client.list_sources())
        for src in sources:
            print(f"- {src.name} (ID: {src.id})")

        print("\nFetching past sessions...")
        active_sessions = []
        for session in client.list_sessions():
            if session.state in (SessionState.CREATED, SessionState.RUNNING):
                active_sessions.append(session.name)

        print(f"Found {len(active_sessions)} active sessions.")
        for s in active_sessions[:5]: # Print up to 5
            print(f"Active Session: {s}")

if __name__ == "__main__":
    main()
