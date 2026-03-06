# How to attach sources

When asking Jules to perform tasks, you need to provide the context where Jules will operate. You can attach a source to your session to give Jules the required code and context.

This guide explains how to define a `SourceContext` and use it to attach a GitHub repository to a new session.

## Defining the source context

To add a source to a session, create a `SourceContext` object and configure the specific source you want to target.

When using GitHub, you'll need a `GitHubRepoContext` to specify the starting branch. Provide the `source` as `sources/github/{owner}/{repo}` to the `SourceContext`.

```python
from jules.models import SourceContext, GitHubRepoContext

# Configure source to be the requested repository
source_context = SourceContext(
    source="sources/github/davideast/jules-sdk-python",
    github_repo_context=GitHubRepoContext(
        starting_branch="main"
    )
)
```

## Attaching the source context

When you call `client.create_session`, pass the configured `source_context` to the method. The session will use the specified source to retrieve code and complete your prompt.

```python
from jules import JulesClient
from jules.models import SourceContext, GitHubRepoContext

def main() -> None:
    with JulesClient() as client:
        # Define the source context
        source_context = SourceContext(
            source="sources/github/davideast/jules-sdk-python",
            github_repo_context=GitHubRepoContext(
                starting_branch="main"
            )
        )

        # We need to add the source_context parameter to create_session
        session = client.create_session(
            prompt="Write a hello world program in Python",
            source_context=source_context
        )
        print(f"Session created: {session.name} (State: {session.state.value})")

if __name__ == "__main__":
    main()
```

If you don't need a `SourceContext` object, you can pass a string directly to the `source` keyword argument when creating a session, and Jules will map it to a default source context.
