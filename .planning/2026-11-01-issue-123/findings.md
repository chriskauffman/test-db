# Findings & Decisions

## Requirements
- Issue 123 requests tests for foreign-database rejection, wrong encryption key, and deleting a person with a job.
- Existing unrelated worktree change: `tests/data/test_schema_v1.sqlite`; preserve it.
- The foreign-database test already exists in `tests/test_database_controller.py` and verifies both the exception and file preservation.

## Research Findings
- Current branch is `main`, synchronized with `origin/main` after PR #142 merged.
- `DatabaseController` raises `ValueError("wrong database encryption key")` when the encryption check fails.
- `Job.person` is a cascading foreign key, so `Person.destroySelf()` should remove a related job without error.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| One requested test already exists | Avoid duplicate coverage; add only the two missing tests. |

## Resources
-
