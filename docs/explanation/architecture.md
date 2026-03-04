# Architecture and Design

The Jules Python SDK is designed to provide an idiomatic, accessible interface to the Jules API. This document explains the core architectural decisions behind the SDK, focusing on the choice of synchronous communication, the necessity of polling, and the polymorphic design of the `Activity` model.

## Synchronous SDK for an Asynchronous API

The Jules API (`v1alpha`) operates asynchronously. When you create a session, the backend immediately returns a session object in a `CREATED` or `QUEUED` state, while the actual work is performed asynchronously in the background.

Despite this asynchronous backend, the Jules Python SDK is fundamentally synchronous, utilizing the `httpx` library for blocking HTTP requests. This design choice prioritizes developer experience and ease of integration in the most common Python environments.

### Why `httpx` and Synchronous Execution?

1.  **Simplicity and Accessibility:** The primary goal of the SDK is to make integrating Jules as straightforward as possible. A synchronous API lowers the barrier to entry, allowing developers to write simple scripts or integrate with traditional WSGI frameworks (like Django or Flask) without needing to manage event loops or `async`/`await` primitives.
2.  **State Management:** An asynchronous SDK would push the complexity of state management onto the user. By keeping the SDK synchronous, users can reason about their code sequentially. When a method returns, the operation it represents is complete (from the SDK's perspective), even if the backend is still processing the broader session.
3.  **Broad Compatibility:** While asynchronous frameworks (like FastAPI) are popular, a vast amount of Python code remains synchronous. A synchronous SDK can be used in almost any Python environment, whereas an asynchronous SDK requires a compatible event loop.

## Polling vs. Webhooks

Because the backend is asynchronous and the SDK is synchronous, the SDK relies on polling to track the progress of a session. This is why users must repeatedly call methods like `get_session()` and `list_activities()`.

### The Necessity of Polling

When a session is created, the initial response does not contain the final result. To determine when the session has reached a terminal state (e.g., `COMPLETED` or `FAILED`), the SDK must query the API for the current state.

Similarly, as a session progresses, it generates various activities (e.g., `planGenerated`, `agentMessaged`). The SDK must poll the activities endpoint to retrieve these updates.

### Design Considerations

While webhooks are often preferred for real-time updates from asynchronous systems, they introduce significant complexity for the consumer:

1.  **Infrastructure Requirements:** Webhooks require the consumer to host a publicly accessible endpoint to receive callbacks. This is often impractical for local development, scripts, or internal tools.
2.  **Security:** Webhook endpoints must be secured to ensure they are only triggered by legitimate sources.
3.  **Delivery Guarantees:** The consumer must implement logic to handle missed or duplicate webhooks.

Polling, while potentially less efficient in terms of network requests, is entirely self-contained. The SDK controls when and how often it queries the API, eliminating the need for complex infrastructure or callback management. This approach aligns with the goal of providing a simple, out-of-the-box experience.

## Polymorphic `Activity` Model

The Jules API represents activities using one-of JSON fields. For example, an activity might contain a `userMessaged` object *or* a `planGenerated` object, but not both.

To provide a clean, object-oriented interface, the SDK uses a polymorphic design pattern for the `Activity` model.

### Mapping One-Of Fields

Instead of exposing a model with numerous optional fields (where only one is ever populated), the `Activity` class synthesizes these one-of fields into a consistent structure:

1.  **`ActivityType` Enum:** The SDK defines an `ActivityType` enum that corresponds to the possible one-of fields (e.g., `AGENT_MESSAGED`, `PLAN_GENERATED`).
2.  **Type Identification:** When the SDK parses a JSON response, it identifies which one-of field is present and assigns the corresponding `ActivityType` to the `type` property of the `Activity` instance.
3.  **The `details` Property:** The actual payload of the one-of field (the specific data for that activity type) is stored in a generic `details` dictionary.

This design allows developers to write robust code that switches on the `type` property and accesses the relevant data from the `details` dictionary, without needing to check for the existence of every possible one-of field.

```python
# Conceptual Example of Polymorphic Handling
if activity.type == ActivityType.PLAN_GENERATED:
    plan_data = activity.details
    # Process the plan data
```

By abstracting the API's one-of structure, the SDK provides a more Pythonic and predictable model for interacting with session activities.
