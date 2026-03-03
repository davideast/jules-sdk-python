"""Interactive chat session using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/interactive_chat.py
"""
import sys
from jules import JulesClient
from jules.models import SessionState

def main() -> None:
    try:
        with JulesClient() as client:
            print("Creating an interactive chat session...")
            session = client.create_session(prompt="I need help understanding python dataclasses.")
            print(f"Session created: {session.name}")

            print("Simulating a conversation. Sending follow-up message...")
            # Note: This requires the send_message bug to be fixed first
            client.send_message(session.name, "Can you provide a small example?")

            print("\nRecent activities:")
            # List activities is a generator, so we convert to a list
            activities = list(client.list_activities(session.name))
            for activity in activities[-3:]: # Get last 3 activities
                print(f"- Activity: {activity.name} (Type: {getattr(activity, 'activity_type', 'Unknown')})")

            print("\nCleaning up...")
            client.delete_session(session.name)
            print("Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
