# Findings & Decisions

## Requirements
- Keep the existing v1-to-v2 upgrades and destructive confirmation.
- Make PostgreSQL and SQLite failures roll back explicitly.
- Make MariaDB upgrades safe to retry after a partial DDL failure.
- Preserve the current final schema and removal of obsolete encryption data.

## Research Findings
- `_upgrade()` executes SQLite with `executescript()` and splits PostgreSQL/MariaDB scripts on semicolons, then commits once.
- PostgreSQL and SQLite migration scripts contain explicit `BEGIN`/`COMMIT`; the exception path currently does not call rollback.
- MariaDB DDL commits implicitly, so a failed statement can leave earlier constraint changes applied.
- The MariaDB migration has two foreign-key replacement steps followed by idempotent table/data cleanup; foreign-key replacement is the non-idempotent portion.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Keep SQL assets for PostgreSQL/SQLite and add explicit rollback | These backends can provide transactional migration behavior. |
| Execute MariaDB foreign-key changes conditionally from schema metadata | MariaDB cannot roll back DDL; checking the current rule makes interrupted upgrades retryable. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-

## Review: 2026-11-12
- No confirmed correctness, safety, scale, or lean findings in the current upgrade changes.
- SQLite upgrade behavior is exercised end-to-end; the full `make build` passed with 233 tests passing and 1 skipped.
- PostgreSQL and MariaDB live migration behavior was not run in this environment. MariaDB retry handling has unit coverage using a mocked cursor, while the real integration test remains opt-in and destructive.
