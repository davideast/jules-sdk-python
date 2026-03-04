# Session states

When you create a Jules session, it moves through several states during its execution. The `SessionState` enum in `jules.models` reflects these states.

## Valid States

*   **`STATE_UNSPECIFIED`**: An unknown or invalid state.
*   **`CREATED`**: The session has been created.
*   **`QUEUED`**: The session is queued for execution but has not yet started.
*   **`RUNNING`**: The session is currently executing its plan.
*   **`IN_PROGRESS`**: The session is currently executing its plan.
*   **`PAUSED`**: Execution has been temporarily halted, awaiting user input or approval.
*   **`AWAITING_USER_FEEDBACK`**: Execution is paused and waiting for user input.
*   **`AWAITING_PLAN_APPROVAL`**: Execution is paused and waiting for the user to approve a plan.

## Terminal States

Once a session reaches a terminal state, it can no longer be updated.

*   **`COMPLETED`**: Execution finished successfully.
*   **`FAILED`**: The session encountered a fatal error during execution.
*   **`CANCELLED`**: Execution was manually cancelled.
