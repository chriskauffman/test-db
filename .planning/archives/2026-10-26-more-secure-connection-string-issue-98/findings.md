# Findings & Decisions: Protecting Sensitive Data in Database Connection Strings

Use this file as the durable knowledge base for discoveries, evidence, and decisions.

## Requirements

1. **Protect DB Credentials in Connection Strings**:
   - Database connection strings frequently contain credentials (passwords, usernames, auth tokens, e.g., `postgresql://user:password@localhost:5432/db` or `mysql://user:password@localhost:3306/db`).
   - Credentials must not be exposed in plain text in log files (`tdb.log`, console logs), process listings, or console commands (`cmd2` `set` / `show`).
   - Credential representations in settings and objects must be masked by default (using Pydantic's `SecretStr`).

2. **Maintain Compatibility**:
   - `DatabaseController` must accept either `str` or `SecretStr` as `connectionURI`.
   - CLI flags in `tdb.py` (`-d` / `--db-connection-uri`) must continue functioning with Typer.
   - Interactive console (`tdb-console`) must support setting and switching database connections without revealing secrets on screen or in logs.
   - All existing 181 tests must pass, with 100% type check and lint compliance.

## Research Findings

### 1. Leak Vectors Identified
- **`src/test_db/_cli_settings.py`**:
  `db_connection_uri` is currently typed as `str | None`. In contrast, `database_encryption_key` uses `CliSuppress[SecretStr]`. Whenever `Settings` is dumped, printed, or logged (`logger.debug("settings=%s", settings)` in `tdb.py`), the cleartext URI and password are leaked to disk.
- **`src/test_db/_database_controller.py`**:
  - `DatabaseController.__init__` accepts `connectionURI: str` and logs `logger.debug("connectionURI=%s", self.connectionURI)`, writing cleartext passwords to debug logs.
  - Line 108 checks `if "sqlite" in str(self.connectionURI):`. If `connectionURI` is a `SecretStr`, `str(...)` returns `'**********'`, which fails the sqlite check and skips setting `PRAGMA foreign_keys = ON`.
- **`src/test_db/tdb.py`**:
  Typer CLI does not natively support `SecretStr` parameter annotations (raises `RuntimeError: Type not yet supported: SecretStr`). Therefore, the Typer callback parameter must remain `str | None` (or be wrapped after receipt) and coerced to `SecretStr` before downstream use.
- **`src/test_db/tdb_console.py`**:
  Uses `cmd2.Settable("db_connection_uri", str, ...)` and logs `_param_name=%s, _old=%s, new=%s` and `resetting db with db_connection_uri=%s`. `cmd2.Settable` supports `SecretStr` as `val_type`: when configured with `SecretStr`, `cmd2` converts input to `SecretStr` and displays `'**********'` in the `set` listing and parameter inspection.
- **`tests/cli/conftest.py`**:
  Sets `os.environ["DB_CONNECTION_URI"] = temporary_db.connectionURI`. If `temporary_db.connectionURI` is a `SecretStr`, assigning directly to `os.environ` fails with a `TypeError` unless `.get_secret_value()` is called.
- **`tests/test_database_options.py`**:
  Present in the repository but 0 bytes (empty). Ideal location for new unit tests targeting secure connection string handling and `Settings` options.

### 2. Standard Database Config Files (`~/.pgpass`, `~/.my.cnf`)
- **PostgreSQL (`~/.pgpass` / `$PGPASSFILE`)**:
  - `libpq` and `psycopg` automatically consult `~/.pgpass` (permissions `0600`, format `hostname:port:database:username:password`) when no password is provided in connection parameters.
  - SQLObject's `PostgresConnection` translates `postgresql://user@host:port/database` into `dsn_dict = {'host': ..., 'port': ..., 'dbname': ..., 'user': ...}` omitting `password` entirely. When `psycopg.connect(**self.dsn_dict)` is called without a password, `~/.pgpass` supplies the credentials transparently with zero code changes needed.
- **MySQL / MariaDB (`~/.my.cnf` / `~/.mylogin.cnf`)**:
  - MySQL C client (`libmysqlclient` / `MariaDB Connector/C` used by `mysqlclient`) automatically reads `~/.my.cnf` (`[client]` section) by default when connecting without password.
  - SQLObject passes query parameters in the URI directly into `conn.kw` in `mysqlclient.connect(...)`. For example, `mysql://user@host/database?read_default_file=~/.my.cnf&read_default_group=client` is supported natively by SQLObject.
- **Recommendation (Defense-in-depth)**:
  - Standard config files (`.pgpass` and `.my.cnf`) and connection string protection (`SecretStr`) are complementary, not mutually exclusive:
    1. Standard config files eliminate the need to put passwords in connection strings/environment variables in the first place.
    2. `SecretStr` ensures that if a password *is* embedded in a connection string (e.g. legacy configs, CI/CD pipelines, Docker environments, or user convenience), it is never exposed in logs, outputs, or error traces.
    3. Documenting `.pgpass` and `.my.cnf` usage provides users with clear security best practices for multi-database environments.

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Use `pydantic.SecretStr` for `Settings.db_connection_uri` | Follows the existing codebase idiom established by `database_encryption_key`. Automatically masks secrets in `repr()`, `str()`, and serialized outputs. |
| Accept `str | SecretStr` in `DatabaseController.__init__` | Backward-compatible for callers passing strings while supporting `SecretStr` natively. |
| Store `self.connectionURI` as `SecretStr` in `DatabaseController` | Ensures `logger.debug("connectionURI=%s", self.connectionURI)` and attribute inspection do not leak credentials. |
| Use `self.connectionURI.get_secret_value()` for SQLObject and scheme checks | SQLObject expects a plain string URI. Using `.get_secret_value()` explicitly unwraps the secret only where required. |
| Configure `cmd2.Settable("db_connection_uri", SecretStr, ...)` in `tdb_console.py` | Automatically masks credentials in console display (`set` output) and when logging setting changes. |
| Keep Typer callback parameter as `str | None` and coerce to `SecretStr` | Prevents Typer runtime crashes while ensuring internal code paths operate on protected `SecretStr`. |

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| Typer raises `RuntimeError: Type not yet supported: SecretStr` on CLI options | Keep Typer callback parameter typed as `str | None` and wrap with `SecretStr` inside the function body. |
| `"sqlite" in str(self.connectionURI)` returns `False` when `SecretStr` is used | Check `if "sqlite" in self.connectionURI.get_secret_value():` instead of `str(...)`. |
| `os.environ[...] = temporary_db.connectionURI` requires a `str` | Use `.get_secret_value()` when exporting to environment variables. |

## Resources

- SQLObject URI connection documentation: `sqlobject.connectionForURI`
- Pydantic `SecretStr`: `https://docs.pydantic.dev/latest/concepts/types/#secret-types`
- cmd2 `Settable`: `https://cmd2.readthedocs.io/en/latest/features/settables.html`
