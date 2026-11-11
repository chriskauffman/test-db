# Findings & Decisions

## Requirements
- Issue context is unavailable through GitHub CLI/web in this environment; the checked-out branch is `FEAT/remove-notFoundError`, which identifies the requested change.
- Remove the internal `NotFoundError` adapter while preserving CLI exit behavior, console error behavior, and key-specific missing-key messages.

## Research Findings
- `NotFoundError` is referenced only by `src/test_db/_lookup.py`, `src/test_db/cli/_validate.py`, `src/test_db/console/_base_command_set.py`, `tests/test_lookup.py`, and README examples.
- `lookup()` only translates `Invalid` and `SQLObjectNotFound`; it has no other behavior.
- `get_key_value()` is only used by the CLI and console validators and can retain its missing-key message using the native exception.
- Existing tests cover the CLI/console behavior and must remain unchanged; the dedicated `_lookup` unit test should be replaced with boundary-focused coverage if needed.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Catch native `Invalid` and `SQLObjectNotFound` in validators | Avoid an internal exception type while preserving current user-facing behavior. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-
