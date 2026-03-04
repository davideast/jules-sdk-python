---
milestone: "3"
---
# Markdown Documentation (Diátaxis)

Write documentation for the Jules SDK organized according to the [Diátaxis framework](https://diataxis.fr/) — four distinct documentation types, each serving a different user need. Files live in `docs/tutorials/`, `docs/how-to/`, `docs/reference/`, and `docs/explanation/`, with `README.md` at the repo root as the entry point.

## Diagnostics
- Existing docs: `find docs/ -name "*.md" | sort`
- Current README: `cat README.md`
- Validate internal links: `markdown-link-check README.md docs/**/*.md`
- Check snippets exist: `find examples/ -name "*.py" | sort`

## Tools
- API Discovery Doc: `curl -s https://jules.googleapis.com/$discovery/rest?version=v1alpha`
- SDK source: `cat src/jules/client.py`
- SDK models: `cat src/jules/models.py`
- Existing snippets: `find examples/ -name "*.py" -exec cat {} +`

## The Four Documentation Types

Diátaxis defines four distinct documentation types. Before writing anything, identify which type it is — and hold to only that type. Mixing them is the root cause of most documentation problems.

| Type | User need | User state | Key question to ask yourself |
|------|-----------|------------|------------------------------|
| Tutorial | Acquire skills through doing | Learning | Am I teaching, or am I telling? |
| How-to guide | Accomplish a specific goal | Working | Does this address a real problem a competent user would have? |
| Reference | Look up facts about the machinery | Working | Am I describing, or am I explaining? |
| Explanation | Understand the why and how | Studying | Am I adding context, or am I instructing? |

## Assessment Hints

Start by reading the SDK source (`src/jules/client.py`, `src/jules/models.py`) and all existing snippets in `examples/`. The snippets from milestone 2 are your primary usage evidence.

For each assessment, identify which Diátaxis quadrant is most underserved and produce one document that fills it. Work from the inside out — don't try to build a complete structure upfront. Each document should serve a single, identifiable user need.

### Tutorials (`docs/tutorials/`)

A tutorial is a **lesson**. The user is a learner; you are the instructor. Your job is to ensure their success. Tutorials are practical — the user does things — but the goal is what they *learn*, not just what they produce.

Qualities of a good tutorial:
- Starts from a known state, ends at a known state
- Every step works — no "your output may vary"
- Explains what is happening at each step, briefly, without distracting from the doing
- Does not explain *why* things work the way they do (that belongs in explanation)
- Does not show all possible options (that belongs in reference)

Suggested tutorial for Jules:
- **`docs/tutorials/first-session.md`** — From `pip install` to a completed session. The user creates a client, submits a task, watches it run, and reads the result. They learn what a session *feels like* before understanding what it *is*.

### How-to Guides (`docs/how-to/`)

A how-to guide addresses a **real-world goal or problem**. The user is already competent; they don't need to be taught. They need directions. Write from the user's perspective, not the SDK's.

Qualities of a good how-to guide:
- The title names the goal, not the tool: "How to wait for a session to finish", not "Using the poll method"
- Assumes baseline competence — skip obvious steps
- May fork and require judgment; not all problems are linear
- Links to reference for exhaustive details, rather than including them

Suggested how-to guides for Jules:
- **`docs/how-to/poll-to-completion.md`** — How to wait for a session to reach a terminal state, including timeout handling.
- **`docs/how-to/approve-a-plan.md`** — How to inspect plan steps and approve or reject before execution begins.
- **`docs/how-to/handle-errors.md`** — How to catch `JulesAPIError`, distinguish retryable from fatal errors, and recover gracefully.
- **`docs/how-to/attach-sources.md`** — How to attach source context to a session before submitting.

### Reference (`docs/reference/`)

Reference material **describes the machinery**. It is consulted, not read. Write neutrally — no instruction, no explanation, no opinion. If a method exists, it appears here; if a field has a type, state it.

Qualities of good reference:
- Structure mirrors the SDK's structure (module → class → method)
- States facts: types, defaults, constraints, error conditions
- Uses brief examples only to illustrate usage, not to teach
- Austere — every word earns its place

Suggested reference pages for Jules:
- **`docs/reference/client.md`** — `JulesClient`: constructor parameters, context manager behavior, all public methods with signatures, parameters, return types, and exceptions raised.
- **`docs/reference/models.md`** — All model classes (`Session`, `Plan`, `PlanStep`, etc.): fields, types, and allowed values.
- **`docs/reference/errors.md`** — `JulesAPIError` and its subclasses: when each is raised, which are retryable, and what attributes they carry.
- **`docs/reference/session-states.md`** — Enumeration of all session lifecycle states, valid transitions, and terminal states.

### Explanation (`docs/explanation/`)

Explanation provides **context and understanding**. The user is studying, not working. Explanation answers *why*, illuminates design decisions, and joins things together. It can take perspectives and circle around its subject.

Qualities of good explanation:
- Does not instruct — link to how-to guides for that
- Does not list facts — link to reference for that
- Helps the reader build a mental model
- Can discuss tradeoffs, history, or the reasoning behind an API design

Suggested explanations for Jules:
- **`docs/explanation/sessions.md`** — What a session is, why the plan-gated model exists, and how the lifecycle was designed to support long-running async tasks.
- **`docs/explanation/sources.md`** — What sources represent, how Jules uses them to scope execution, and why they are separate from the task description.

## README.md

The README is not a Diátaxis document — it is a **signpost**. Its job is to orient a new developer and get them to the right document as fast as possible. Keep it short.

```markdown
# Jules SDK for Python

one-line description

## Installation

pip install jules-sdk

## Quickstart

the shortest possible working example — ideally 5–10 lines

## Documentation

**Learning Jules**
- [Your first session](docs/tutorials/first-session.md) — start here

**Doing things**
- [Wait for a session to finish](docs/how-to/poll-to-completion.md)
- [Approve a plan](docs/how-to/approve-a-plan.md)
- [Handle errors](docs/how-to/handle-errors.md)
- [Attach sources](docs/how-to/attach-sources.md)

**Looking things up**
- [JulesClient](docs/reference/client.md)
- [Models](docs/reference/models.md)
- [Errors](docs/reference/errors.md)
- [Session states](docs/reference/session-states.md)

**Understanding Jules**
- [How sessions work](docs/explanation/sessions.md)
- [How sources work](docs/explanation/sources.md)
```

## Insight Hints
- After writing each document, identify which quadrant it actually ended up in — if it drifted (a tutorial that instructs without teaching, a how-to that explains too much), flag it for revision
- Report which SDK methods and model fields have no corresponding reference entry
- Note which user problems from the snippets have no corresponding how-to guide

## Verification

After writing each document:
- All code blocks are syntactically valid Python (copy-paste runnable with a valid key)
- All internal links resolve: `markdown-link-check README.md docs/**/*.md`
- No placeholder text: `grep -rn "TODO\|TBD\|<fill" README.md docs/`
- Each document is clearly one Diátaxis type — if you can't identify which quadrant it belongs to, it needs to be split or refocused

### When something is missing

If a doc references a snippet that doesn't exist, or an API feature with no SDK coverage, note it in `docs/_gaps.md` rather than writing speculative documentation. This file is internal and should not be linked from the README.

## Constraints
- `README.md` at repo root; topic docs in `docs/{type}/{topic}.md` (lowercase, hyphenated)
- Tutorials and how-to code examples must be drawn from actual `examples/` snippets
- Reference docs must describe the SDK as it actually exists — no aspirational content
- Explanation docs must not instruct; how-to guides must not explain beyond what's needed for the task
- Do not document private SDK methods (anything prefixed with `_`)
