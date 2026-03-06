# How sessions work

A session is the fundamental unit of work in Jules. It represents a single conversation or task execution between you and the Jules AI agent.

## The session lifecycle

When you submit a prompt to Jules, it does not execute immediately and return the final answer. Instead, the task is wrapped in a session object and queued.

Because AI agents take time to clone repositories, read code, formulate plans, and make changes, Jules uses an asynchronous architecture. The session moves through a defined lifecycle, communicating its progress through states:

1.  **Creation**: The session is created (`CREATED`) and scheduled for execution (`QUEUED`).
2.  **Execution**: Jules starts analyzing the source repository and working on the task (`RUNNING` or `IN_PROGRESS`).
3.  **Completion**: The task finishes, either successfully (`COMPLETED`), failing due to an error (`FAILED`), or being cancelled (`CANCELLED`).

As a user, you interact with this architecture by polling the session for updates until it reaches a terminal state.

## Plan-gated execution

Jules has the ability to write code and commit changes to your repositories. Because this is a powerful capability, Jules includes a plan-gating feature.

Before making any changes, Jules first generates an execution plan outlining the steps it intends to take. By default, it proceeds directly to executing these steps. However, by setting `require_plan_approval=True` when creating a session, you instruct Jules to pause (`AWAITING_PLAN_APPROVAL`) once the plan is ready.

This design gives you explicit control over the AI's actions. You can review the proposed changes, evaluate the logic, and decide whether to approve (`approve_plan`) the task, or abort it entirely before any side effects occur.
