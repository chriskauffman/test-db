# Task Plan: Enhance DB Connection String to Protect Secret Data

Use this file as the durable roadmap for the task. Create it before complex work and keep it current as phases change.

## Goal

Enhance database connection string handling across Settings, DatabaseController, CLI, and console interfaces to protect secret credentials from exposure in logs, screen outputs, and error reports using `SecretStr`.

## Next Step

Completed all phases. Ready for final review.

## Current Phase

Phase 5: Delivery & Review

## Phases

### Phase 1: Requirements & Discovery
- [x] Survey codebase for DB connection string usage and sensitive data exposure vectors
- [x] Investigate SQLObject, Typer, Pydantic, and cmd2 behavior with `SecretStr`
- [x] Document leak vectors and architectural requirements in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define technical approach and component contracts
- [x] Establish backward compatibility strategy for `str` and `SecretStr`
- [x] Create detailed task plan and progress tracking files
- **Status:** complete

### Phase 3: Implementation
- [x] Update `src/test_db/_cli_settings.py` to use `SecretStr` for `db_connection_uri`
- [x] Update `src/test_db/_database_controller.py` to accept `str | SecretStr`, store as `SecretStr`, unwrap for SQLObject, and fix SQLite foreign key check
- [x] Update `src/test_db/tdb.py` to coerce CLI connection URI to `SecretStr`
- [x] Update `src/test_db/tdb_console.py` to use `SecretStr` in cmd2 `Settable` and mask logging
- [x] Update `tests/cli/conftest.py` fixture to safely unwrap `SecretStr` for environment variable export
- [x] Update `README.md` to document using `~/.pgpass` and `~/.my.cnf` for passwordless database connections
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Implement unit and integration tests in `tests/test_database_options.py` testing `SecretStr` masking and connection handling
- [x] Run full test suite (`uv run pytest` - 187 passed)
- [x] Run type checking (`uv run ty check` - 100% passed)
- [x] Run linter and formatting checks (`uv run ruff check`, `uv run pydoclint`, `uv run ruff format --check` - 100% passed)
- **Status:** complete

### Phase 5: Delivery & Review
- [x] Review git diff and working tree state
- [x] Update progress.md with complete session log and test outcomes
- [x] Present changes and verification results to user
- **Status:** complete

## Key Questions

1. Should `db_connection_uri` in `Settings` be `SecretStr` or `CliSuppress[SecretStr]`?
   - *Answer:* `SecretStr` is sufficient and matches `database_encryption_key`, ensuring logs and serialized configs mask the credentials.
2. How should Typer CLI options handle `SecretStr` without crashing?
   - *Answer:* Typer option remains annotated as `str | None` to prevent click/typer crashes, and is converted to `SecretStr` within the function callback.
3. How should `DatabaseController.connectionURI` behave for existing consumers?
   - *Answer:* Accepts both `str` and `SecretStr`, stores internally as `SecretStr`, and provides `.get_secret_value()` for driver connections while masking on `str()`, `repr()`, and logging.
4. Should we support standard database config files (`~/.pgpass`, `~/.my.cnf`)?
   - *Answer:* Yes! SQLObject and underlying drivers (`psycopg`, `mysqlclient`) natively support passwordless URIs (`postgresql://user@host/db`, `mysql://user@host/db`) that resolve passwords from `~/.pgpass` or `~/.my.cnf`. Pairing this with `SecretStr` provides defense-in-depth: users can omit passwords entirely, but if passwords are supplied in connection strings, they remain protected.

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Use `pydantic.SecretStr` for `Settings.db_connection_uri` | Ensures all settings dumps, prints, and log entries mask DB passwords automatically. |
| Accept `str | SecretStr` in `DatabaseController` and store as `SecretStr` | Provides seamless backward compatibility while ensuring debug logs (`logger.debug("connectionURI=%s", ...)`) never leak passwords. |
| Use `.get_secret_value()` for `sqlobject.connectionForURI()` | Unwraps credentials only when handing off to the low-level database driver. |
| Use `SecretStr` in `cmd2.Settable` for console | Masks connection string in console `set` listings and parameter change logs. |
| Adopt defense-in-depth with `.pgpass` / `.my.cnf` support | Encourages passwordless connection strings via native DB client config files while guaranteeing that connection strings with embedded passwords cannot leak. |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| Typer raises `RuntimeError: Type not yet supported: SecretStr` when `SecretStr` is used as a CLI option | 1 | Keep CLI option parameter typed as `str | None` in Typer callback, then convert to `SecretStr` inside the callback body. |
| `"sqlite" in str(self.connectionURI)` returns `False` if `self.connectionURI` is `SecretStr` | 1 | Check `if "sqlite" in self.connectionURI.get_secret_value():` so SQLite foreign key pragma continues to be executed. |
| Ruff I001 import block unsorted in `tests/test_database_options.py` | 1 | Separated standard library `import logging` from third-party `from pydantic import SecretStr` with empty line. |

## Notes

- Update phase status as work progresses: `pending` to `in_progress` to `complete`.
- All 181 existing tests must continue to pass.
- Code must pass `uv run ty check`, `uv run ruff check`, and `uv run pydoclint`.
