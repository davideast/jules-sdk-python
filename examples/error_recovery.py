"""Handling API errors effectively using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/error_recovery.py
"""
import sys
from jules import JulesClient
from jules.client import JulesAPIError

def main() -> None:
    print("Attempting to connect with an invalid API key to trigger an error...")
    try:
        with JulesClient(api_key="invalid-key-for-testing") as client:
            list(client.list_sessions())

    except JulesAPIError as err:
        print(f"Caught an expected API Error!")
        print(f"Status Code: {err.status_code}")
        print(f"Error Message: {err}")
        if err.status_code == 403 or err.status_code == 401:
            print("Tip: Check your JULES_API_KEY environment variable.")
            sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
