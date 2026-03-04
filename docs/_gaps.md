# Documentation Gaps

This document tracks known missing functionality, API methods without examples, and unwritten documentation.

## Missing API Coverage
The following methods in `JulesClient` do not have dedicated how-to guides or code examples:

*   `send_message()` - Used in chat sessions, but there's no how-to.
*   `archive_session()` - No how-to guide for archiving sessions.
*   `unarchive_session()` - No how-to guide for unarchiving.
*   `get_activity()` - No explicit how-to.
*   `list_activities()` - No explicit how-to.
*   `delete_session()` - Used in examples as cleanup, but no dedicated section.

## Missing Models Coverage
The following models or fields could use more explanation:
*   `SessionOutput` and `ChangeSet` (How to retrieve code patches/PR links from a session).

## Missing Examples
*   `examples/sources.py` is referenced in tests/verification steps but does not exist in the repository (`examples/inspect_source.py` exists instead).
