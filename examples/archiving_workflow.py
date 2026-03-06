"""Archiving and unarchiving sessions using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/archiving_workflow.py
"""
from jules import JulesClient

def main() -> None:
    with JulesClient() as client:
        print("Creating a temporary session to demonstrate archiving...")
        session = client.create_session(prompt="Generate a quick sorting algorithm")
        print(f"Session created: {session.name}")

        print("Archiving the session...")
        client.archive_session(session.name)
        print("Session archived successfully.")

        print("Unarchiving the session...")
        client.unarchive_session(session.name)
        print("Session unarchived successfully.")

        print("Cleaning up...")
        client.delete_session(session.name)
        print("Done.")

if __name__ == "__main__":
    main()
