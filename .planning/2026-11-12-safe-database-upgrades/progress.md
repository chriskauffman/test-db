# Progress Log

## Session: 2026-11-12

### Current Status
- **Phase:** 1 - Requirements & Discovery
- **Started:** 2026-11-12

### Actions Taken
- Inspected the upgrade runner, all v1-to-v2 migration scripts, and migration tests.
- Changed upgrades to execute statements uniformly and explicitly roll back failures.
- Added SQLite foreign-key restoration after failed upgrades.
- Added MariaDB metadata checks so completed foreign-key steps are skipped on retry.
- Added focused coverage for completed MariaDB constraint steps.
- Added SQLite rollback coverage and moved transaction control out of SQL assets.
- Added raw-connection schema validation before commit and regression coverage for validation rollback.

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| `tests/test_database_controller.py` | pass | 22 passed | pass |
| Ruff format/check | pass | passed | pass |
| `make build` | pass | stopped at `ty check` on nullable regex match | fixed and rerunning |
| `make build` retry | pass | 4 tests failed because rollback test polluted shared in-memory DB | isolated test database and rerunning |
| `make build` final | pass | 232 passed, 1 skipped; lint, type-check, audit, schema generation, and package build passed | pass |
| `make build` after pre-commit validation | pass | 233 passed, 1 skipped; all checks passed | pass |

### Errors
| Error | Resolution |
|-------|------------|
| `ty` rejected calling `.group()` on a nullable regex match | Store `drop or add` in a narrowed local before calling `.group()`. |
| Rollback test changed cached in-memory schema version for later tests | Use a unique temporary file-backed SQLite database. |
