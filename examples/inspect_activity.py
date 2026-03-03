"""Inspecting detailed session activities using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/inspect_activity.py
"""
from jules import JulesClient
from jules.models import ActivityType

def main() -> None:
    with JulesClient() as client:
        print("Finding a session to inspect...")
        sessions = list(client.list_sessions())
        if not sessions:
            print("No sessions found. Try running getting_started.py first.")
            return

        session = sessions[0]
        print(f"Inspecting activities for session: {session.name}")

        activities = list(client.list_activities(session.name))
        if not activities:
            print("No activities found in this session.")
            return

        # Pick the first activity to inspect deeply
        target_activity = activities[0]
        print(f"\nFetching detailed activity: {target_activity.name}")

        # In a real app, you might receive the activity name from a webhook
        activity = client.get_activity(target_activity.name)

        print(f"Type: {activity.type.value}")
        print(f"Created: {activity.create_time}")
        print(f"Originator: {activity.originator or 'Unknown'}")
        print(f"Description: {activity.description or 'None'}")

        # Demonstrate unpacking the type-specific details
        print("\nActivity Details:")
        if activity.type == ActivityType.AGENT_MESSAGED:
            message = activity.details.get("message", {})
            print(f"Agent said: {message.get('text', 'No text')}")
        elif activity.type == ActivityType.USER_MESSAGED:
            message = activity.details.get("message", {})
            print(f"User said: {message.get('text', 'No text')}")
        else:
            print(f"Raw details: {activity.details}")

if __name__ == "__main__":
    main()
