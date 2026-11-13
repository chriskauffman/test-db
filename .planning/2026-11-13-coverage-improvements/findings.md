# Findings & Decisions

## Requirements
- Create a separate branch for coverage improvements without changing the current `main` checkout contents.
- Prioritize the skipped migration test and low-coverage interactive view paths identified by `make coverage`.

## Research Findings
- The worktree is clean on `main` at `origin/main`.
- Issue #127 is already merged into `main`; the new branch can start from current `main`.
- Existing console tests did not directly exercise the shared interactive view input loops or entity view edit/detail flows.
- Added tests for BaseView input validation, all entity view edit/detail methods, and PersonView delete confirmation.
- Full coverage run: 243 passed, 1 skipped; total coverage increased from 91% to 93%.
- View coverage after the tests: BaseView 90%, AddressView 84%, BankAccountView 78%, DebitCardView 79%, JobView 75%, OrganizationView 81%, PersonView 87%.
- The new `make test` migration step copies `tests/data/test_schema_v1.sqlite`, but `migration_database()` opens the database with `upgrade=False` before `_prepare_v1`; `DatabaseController` correctly rejects that already-old schema.
- `tests/data/test_schema_v2.sqlite` is the correct source fixture: `_prepare_v1` intentionally mutates a valid v2 database into v1 before the upgrade test.
- Added a project-level `connectionForURI` wrapper that supplies `read_default_file=~/.my.cnf` for passwordless MySQL URIs when the file exists; MySQL automatically reads the `[client]` group.
- SQLObject always passes `passwd=""`, which prevents MySQLdb from using the option-file password. The adapter uses a minimal MySQLConnection subclass that omits `passwd` for passwordless MySQL connections.
- The adapted MySQL URI must be registered under both the adapted and original URI cache keys; otherwise `DatabaseController` closes the shared connection after CLI commands, leaving SQLObject instances with `_connection=None`.
- Migration scripts begin with `--` comments; splitting only on semicolons sends those comments to MariaDB as part of the first SQL statement. Strip line comments before splitting migration statements.
- Explicit `read_default_file` options, password-bearing MySQL URIs, PostgreSQL URIs, and SQLite URIs remain unchanged.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| MySQLdb rejected `passwd=None` before reading `~/.my.cnf`. | Omit the `passwd` keyword in the adapter’s MySQLdb call; a read-only probe then connected successfully to `nas02`. |
| `make build` could not resolve `api.osv.dev` for `uv audit`. | All local checks and tests passed; security audit remains network-dependent. |

## Resources
-
