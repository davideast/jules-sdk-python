import os
import httpx
import re

def main():
    api_key = os.environ.get("JULES_API_KEY")
    if not api_key:
        print("Error: JULES_API_KEY environment variable is not set either.")
        return

    client = httpx.Client(
        base_url=os.environ.get("JULES_BASE_URL", "https://jules.googleapis.com/v1alpha"),
        headers={"x-goog-api-key": api_key}
    )

    try:
        response = client.get("/sessions")
        response.raise_for_status()
        data = response.json()
        for session in data.get("sessions", []):
            prompt = session.get("prompt", "")
            if prompt and re.search(r"Fix Issue #(6[6-9])", prompt):
                print(f"Session Name: {session.get('name')}")
                print(f"Prompt: {prompt}")
                print(f"State: {session.get('state')}")
                print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
