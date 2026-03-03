"""Interactive chat session using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/interactive_chat.py
"""
import sys
from jules import JulesClient

def main() -> None:
    try:
        with JulesClient() as client:
            print("Creating an interactive chat session...")
            session = client.create_session(prompt="I need help understanding python dataclasses.")
            print(f"Session created: {session.name}")

            print("Simulating a conversation. Sending follow-up message...")
            client.send_message(session.name, "Can you provide a small example?")

            print("\nRecent activities:")
            # List activities is a generator, so we convert to a list
            activities = list(client.list_activities(session.name))
            for activity in activities[-3:]: # Get last 3 activities
                print(f"- Activity: {activity.name} (Type: {activity.type.value})")

            print("\nCleaning up...")
            # If your Jules API version supports delete_session, it's used here.
            # Otherwise we might use archive_session. We'll check if delete_session exists.
            if hasattr(client, "delete_session"):
                client.delete_session(session.name)
            else:
                client.archive_session(session.name)
            print("Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
