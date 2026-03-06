---
milestone: "3"
---
# Deep Documentation (Diátaxis)

Write deep, comprehensive documentation for the Jules SDK organized according to the [Diátaxis framework](https://diataxis.fr/) — four distinct documentation types, each serving a different user need. The focus is to constantly improve the **depth** of the docs and to grow to cover helpful topics, without sprawling the navigation and categories. Files live in `docs/tutorials/`, `docs/how-to/`, `docs/reference/`, and `docs/explanation/`, with `README.md` at the repo root as the entry point.

## Diagnostics

Before starting new documentation work, assess the current state and structure of the project:

- **File Hierarchy:** `find docs/ -name "*.md" | sort`
- **Current README Signpost:** `cat README.md`
- **Internal Link Health:** `npx markdown-link-check README.md docs/**/*.md`
- **Code Snippet Availability:** `find examples/ -name "*.py" | sort`
- **API Capabilities:** `curl -s https://jules.googleapis.com/$discovery/rest?version=v1alpha`
- **SDK Implementation:** `cat src/jules/client.py` and `cat src/jules/models.py`
- **Snippet Details:** `find examples/ -name "*.py" -exec cat {} +`

## Hints

### The Four Documentation Types
Diátaxis defines four distinct documentation types. Mixing them is the root cause of shallow, confusing documentation. Before writing anything, identify which type it is — and hold strictly to that type, but dive deep.

| Type | User need | User state | Key question to ask yourself |
|------|-----------|------------|------------------------------|
| Tutorial | Acquire skills through doing | Learning | Am I teaching, or am I telling? |
| How-to guide | Accomplish a specific goal | Working | Does this address a real problem a competent user would have? |
| Reference | Look up facts about the machinery | Working | Am I describing, or am I explaining? |
| Explanation | Understand the why and how | Studying | Am I adding context, or am I instructing? |

### Driving Depth Without Sprawl
The core challenge is balancing comprehensive, deep content with clean, usable navigation. Do not clutter the `README.md` or core index files with every minor example.

Instead, employ a hub-and-spoke model for temporal or demonstrative content:
1. **The Core Documentation:** Keep the main `README.md` focused on top-level concepts (e.g., *How to attach sources*, *JulesClient Reference*). These must stay permanently up-to-date.
2. **The "Feed" or "Cookbook":** Create centralized aggregators (e.g., `docs/how-to/cookbook.md` or a "feed" of examples) where specific, narrow integrations are listed (like a daily social post).
3. **Link Backwards:** If an integration topic (e.g., "Using Jules with Flask") is demonstrative only, it should link back to the core API reference for the underlying methods, rather than re-explaining them. This keeps temporal content cleanly separated from permanent machinery.

### Suggested Areas for Deep Dives

#### Tutorials (`docs/tutorials/`)
*   **Deepen the First Session:** Don't just show `create_session()`. Expand the tutorial to cover what happens when the session pauses, how to read a `Plan`, and how to inspect the final `ChangeSet`.

#### How-to Guides (`docs/how-to/`)
*   **Framework Integrations:** Create specific, deep how-to guides or cookbook entries for using the SDK in real-world web applications. Examples include:
    *   **Django:** Writing a management command that kicks off a Jules session.
    *   **Flask:** Exposing an endpoint to list Jules activities via a webhook.
    *   **FastAPI:** Wrapping the Jules SDK in asynchronous endpoints using `anyio` or background tasks.
    *   *Note: Do not over-index on these specific frameworks. Broaden out to CLI tools (Click, Typer) or data pipelines as needed, but centralize them in a cookbook to avoid navigation sprawl.*
*   **Advanced Plan Approval:** Detail exactly how to parse the `PlanStep` models and programmatically reject or approve based on custom validation logic.

#### Reference (`docs/reference/`)
*   **Exhaustive Detail:** The current reference docs might list methods, but lack depth. Ensure every parameter, every return type, and every possible raised exception (`JulesError`, `JulesAPIError`, specific HTTP codes) is documented extensively.

#### Explanation (`docs/explanation/`)
*   **Deep Architectural Context:** Why is the SDK synchronous when the API is asynchronous? Explain the design decisions behind the polling models vs webhook architectures.

### Insight Hints
- After writing each document, identify which quadrant it actually ended up in — if it drifted, flag it for revision.
- Ensure integration examples focus on the *intersection* of the SDK and the framework, not just teaching the framework.

## Verification

After writing or updating each document, you must verify the following constraints to ensure the depth didn't break the structure:

- All code blocks are syntactically valid Python (copy-paste runnable with a valid key).
- All internal links resolve: `npx markdown-link-check README.md docs/**/*.md`
- No placeholder text remains: `grep -rn "TODO\|TBD\|<fill" README.md docs/`
- The `README.md` remains concise. If you added 5 framework examples, ensure they are listed under a single "Framework Integrations" link, not as 5 separate main navigation items.
- Reference docs accurately describe the SDK as it actually exists in `src/`. No aspirational content.
- Do not document private SDK methods (anything prefixed with `_`).

### When something is missing
If a doc references an API feature with no SDK coverage, note it in `docs/_gaps.md` rather than writing speculative documentation. This file is internal and should not be linked from the README.
