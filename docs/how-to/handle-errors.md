# How to handle errors

The Jules API uses standard HTTP response codes to indicate the success or failure of an API request. When an error occurs, the SDK raises a `JulesAPIError` or `JulesError`.

This guide covers how to capture and inspect exceptions and how to recover gracefully.

## Catching `JulesAPIError`

The SDK translates HTTP error statuses into `JulesAPIError`. This exception subclass contains the status code and a descriptive message from the API to help you identify what went wrong.

```python
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

        # Check if the error is due to authentication
        if err.status_code == 403 or err.status_code == 401:
            print("Tip: Check your JULES_API_KEY environment variable.")
            sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Retryable vs Fatal Errors

Not all errors require manual intervention. The API relies on common HTTP status codes.

* **401 Unauthorized**: Your API key is invalid or missing. Ensure `JULES_API_KEY` is set in your environment. This is a **fatal error**.
* **403 Forbidden**: Your account lacks permissions to access a resource (e.g. you're trying to inspect another user's session). This is a **fatal error**.
* **404 Not Found**: A session or source you requested could not be found. Check your session IDs or ensure you didn't previously delete the resource. This is a **fatal error**.
* **429 Too Many Requests**: You have hit your rate limit. This is a **retryable error**. Wait a bit and try again.
* **5xx Server Error**: Jules is experiencing an internal error. This is usually a **retryable error** (like `502` or `503`), but occasionally requires an investigation.

For network failures or SDK-level issues, such as a timeout, a standard `JulesError` might be raised instead.
