# Findings & Decisions

## Requirements
- Repository: `/Users/ckauffman/Projects/test-db`, Python package managed with `uv`; expected verification is `make build`.
- Work on a dedicated branch; do not commit changes.
- Preserve the pre-existing modification to `tests/data/test_schema_v1.sqlite`.
- Issue 121 title: “Console commands crash with AttributeError after a bad gID”.
- Root cause: console validators print an error and return `None`; callers continue and dereference the missing object.
- Requested fix: raise after `perror` (or let the exception through) and remove caller-side truthiness guards.

## Research Findings
- Current branch is `main`, tracking `origin/main`.
- GitHub issue 121 was retrieved after an approved network retry.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| GitHub network access unavailable | Continue with local history and repository inspection; record limitation if unresolved. |

## Resources
-
