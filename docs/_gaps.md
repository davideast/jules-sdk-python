# Documentation Gaps

This document tracks known missing functionality, API methods without examples, and unwritten documentation.

## Missing API Coverage
The following methods in `JulesClient` do not have dedicated how-to guides or code examples:
*   `reject_plan()` - The `JulesClient` does not have a method to explicitly reject a plan. If programmatic validation fails, users must delete the session or pause automation instead.

## Missing Models Coverage
The following models or fields could use more explanation:
*   `SessionOutput` and `ChangeSet` (How to retrieve code patches/PR links from a session).

