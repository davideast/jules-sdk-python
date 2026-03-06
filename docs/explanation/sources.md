# How sources work

When you create a Jules session, you are giving the AI an explicit prompt to execute. However, prompts are often contextual — they require code or an environment to be meaningful.

This is where sources come in.

## Scoping execution

A source is a reference to a repository or context. It tells Jules where it should perform its task.

When you pass a `source` (or `source_context`) parameter to `create_session`, you attach the session to a specific environment, usually a GitHub repository.

Jules clones the repository, checks out the specified branch (e.g. `main`), and starts working within that codebase. It analyzes the files, writes code, and potentially pushes changes.

By scoping execution to a single source, Jules can understand the context of your task without you needing to copy-paste the code manually into your prompt. This helps the AI act more autonomously on your behalf.
