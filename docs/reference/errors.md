# Errors

The Jules API uses the standard HTTP response codes to indicate success or failure. The SDK wraps these errors into Python exceptions.

## `JulesError`

The base class for all exceptions raised by the Jules SDK.

It is raised for client-side issues, such as missing API keys, incorrect parameters, and network failures.

## `JulesAPIError`

An exception raised when the API returns an HTTP error status code (e.g., `4xx` or `5xx`).

It inherits from `JulesError`.

### Properties

*   **`message`**: A detailed error message including the response text from the API.
*   **`status_code`**: The integer HTTP status code returned by the API (e.g., 401, 404, 500).

### Common Error Codes

*   `401 Unauthorized`: Authentication failed, usually due to a missing or invalid API key.
*   `403 Forbidden`: You don't have permission to perform the requested action.
*   `404 Not Found`: The requested resource (session, activity, or source) does not exist.
*   `429 Too Many Requests`: Rate limit exceeded. (Retryable)
*   `500 Internal Server Error`: An unexpected error occurred on the server. (Retryable)
*   `502 Bad Gateway` / `503 Service Unavailable`: Temporary network or server issues. (Retryable)
