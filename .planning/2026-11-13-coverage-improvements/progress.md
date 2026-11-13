# Progress Log

## Session: 2026-11-13

### Current Status
- **Phase:** 4 - Testing & Verification
- **Started:** 2026-11-13

### Actions Taken
- Created and pinned the coverage-improvements planning directory.
- Confirmed a clean `main` checkout at `origin/main`.
- Added `tests/test_views.py` covering shared input validation and entity view flows.
- Ran the full coverage suite successfully.
- Reviewed the migration targets: the SQLite target copies the v2 fixture before converting it to v1; PostgreSQL and MySQL targets require disposable databases.
- Added and tested the project-level MySQL connection adapter.
- Full local build checks passed after the adapter: 247 regular tests passed, 1 skipped, and the SQLite migration test passed. `uv audit` could not resolve `api.osv.dev` in the sandbox.
- Verified a read-only MySQL connection to `nas02` succeeds using the credentials from `~/.my.cnf`.
- Reproduced and fixed the MariaDB CLI duplicate-key failures; the focused module now passes 3 tests.
- Reproduced and fixed MariaDB migration parsing of leading SQL comments; the parser regression test and SQLite upgrade test pass.

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| `tests/test_views.py` | All new tests pass | 3 passed | Pass |
| Full coverage suite | Existing tests remain green | 243 passed, 1 skipped | Pass |
| Coverage report | View coverage improves | Total 93% | Pass |
| `test-migration-sqlite` | Migration test runs | 1 passed | Pass |
| MySQL connection probe | Passwordless URI uses `~/.my.cnf` | Connected successfully to `nas02` | Pass |
| MariaDB duplicate-key CLI tests | Shared model connections survive CLI cleanup | 3 passed; SQLObject emits its existing `ping(True)` deprecation warning | Pass |

### Errors
| Error | Resolution |
|-------|------------|
