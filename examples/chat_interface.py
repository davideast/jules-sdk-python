"""Interactive chat workflow using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/chat_interface.py
"""
import time
from jules import JulesClient

def main() -> None:
    with JulesClient() as client:
        print("Starting a new interactive session...")
        session = client.create_session("What are the best practices for Python testing?")
        print(f"Session created: {session.name}")

        print("\nSending a follow-up message...")
        client.send_message(session.name, "Can you focus specifically on pytest?")

        print("\nPolling for activity (agent response)...")
        # In a real app, you would poll or wait for the session state to change
        # For the snippet, we just list current activities
        time.sleep(2)
        activities = list(client.list_activities(session.name))
        for activity in activities:
            print(f"- [{activity.create_time}] {activity.type.value}: {activity.description or 'No description'}")

        print("\nArchiving session to clean up...")
        client.archive_session(session.name)
        print("Session archived.")

if __name__ == "__main__":
    main()
