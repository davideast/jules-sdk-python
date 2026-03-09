"""Watching a session: Polling for real-time progress updates.

Usage:
    export JULES_API_KEY=your-key
    python examples/watch_session.py
"""
import time
from jules import JulesClient
from jules.models import SessionState, ActivityType

def main() -> None:
    with JulesClient() as client:
        print("Creating a new Jules session...")
        session = client.create_session(prompt="Analyze the repository structure")
        print(f"Session created: {session.name}")
        if session.url:
            print(f"View your session here: {session.url}")

        print("\nWatching for progress updates...")
        seen_activities = set()

        while True:
            current_session = client.get_session(session.name)

            # Fetch activities and filter for new ones
            activities = list(client.list_activities(session.name))
            for activity in reversed(activities):
                if activity.name not in seen_activities:
                    seen_activities.add(activity.name)
                    if activity.type == ActivityType.PROGRESS_UPDATED:
                        title = activity.details.get("title", "Update")
                        desc = activity.details.get("description", "")
                        print(f"-> {title}: {desc}")

            if current_session.state in (SessionState.COMPLETED, SessionState.FAILED):
                print(f"-> Session finished with state: {current_session.state.value}")
                break

            time.sleep(2)

        print("\nCleaning up session...")
        client.delete_session(session.name)

if __name__ == "__main__":
    main()
