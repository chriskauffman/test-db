# Findings & Decisions

## Scope

- Branch: `FEAT/issue-153-breaking-change-remove-encryption`
- Base: `main`
- Commit: `5b189c4 feat!: Removing PersonSecureKeyValue and EncryptedPickleCol`
- Issue #153: remove all secure columns, tables, modules, and tests; this is a breaking change requiring a full version upgrade.

## Requirements
-

## Research Findings
- Encryption runtime support and the `cryptography` dependency were removed, but CLI encryption settings remain in `src/test_db/_cli_settings.py`; both entry points still load them, and `DatabaseController` still accepts but ignores `databaseEncryptionKey`.
- README.md still claims encryption support and documents the removed metadata and migration behavior.
- Concrete case: a user sets `DATABASE_ENCRYPTION_KEY`, runs the CLI, and stores a key value. The setting is accepted, but the value is stored through the normal string `KeyValue` path, so the user can believe the database is encrypted when it is not.
- The version is intentionally managed by release-please: the commit is `feat!`, `release-type` is `python`, and the workflow uses the release-please manifest.
- Upgrade wiring is incomplete: `tdb.py` exposes `--upgrade/-u` and forwards it to `DatabaseController`, but `tdb_console.py` has no upgrade option, and `DatabaseController._upgrade()` only rechecks the schema because its migration call remains commented out.
- The current application schema version is now 2; the issue #153 migrations set legacy databases to version 2 after removing the encryption table and metadata.
- The generated `tests/data/test_schema_v1.sqlite` fixture now stores `TestDB_ApplicationSchemaVersion=2`; its filename remains `v1` because the existing Makefile/schema snapshot convention still uses that name.
- The planned automatic upgrade should be authorized in the CLI before constructing `DatabaseController`; `DatabaseController` should receive only the approved boolean and remain independent of terminal prompting.
- The v1→v2 migration must cover both the job foreign-key cascade change and encryption removal, and must update the schema-version key last. A successful return should be followed by `validSchema` verification.
- A schema version is the appropriate migration cursor, but the current single `TestDB_ApplicationSchemaVersion` key is not a complete schema validator or migration history. Prefer a dedicated migration ledger, then run small engine-specific structural invariant checks after opening/upgrading.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Add one engine-specific upgrade script for SQLite, PostgreSQL, and MySQL/MariaDB | Existing migrations use separate SQL files because DDL and transaction behavior differ by engine. |
| Drop `person_secure_key_value` and delete the three encryption metadata keys | The secure values are encrypted data that the current release cannot decode; exact-key deletion removes only obsolete metadata. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Verification

`make build` passed: formatting, lint, pydoclint, yamllint, ty, 231 tests, `uv audit`, and `uv build`.

The CLI test organization now keeps tdb-only modules under `tests/cli/tdb` and tdb-console modules under `tests/cli/tdb_console`; the separated key-value coverage passed independently and in the full build.

## Resources
-

## Follow-up Review

- The standalone issue #153 SQL scripts are not invoked by `DatabaseController`; users must run the engine-specific script themselves before opening a legacy database with the new release.

## Implementation Plan

- Reuse the existing engine-specific SQL migration assets and route them from `DatabaseController` using the connection's database name.
- Make the migration a single logical v1→v2 operation per engine. PostgreSQL and SQLite can use transactions; MySQL/MariaDB must document that DDL commits implicitly and should set version 2 only after every statement succeeds.
- In `tdb`, prompt only when `--upgrade/-u` is present; a negative answer exits before opening the database.
- `tdb-console` should not support upgrades; it should continue constructing `DatabaseController` with `upgrade=False` and refuse databases whose schema version is not current.
- Test both accepted and declined confirmation paths, the controller's version dispatch, and a SQLite v1 fixture that proves the table/foreign-key changes and version update.
- Implemented and verified: the controller dispatches bundled engine-specific migrations, checks required tables/removal/cascade invariants, and the Typer CLI confirms before upgrade. `tdb-console` remains refusal-only.
- PostgreSQL upgrades were falsely reported as failed because invariant validation selected `tc.table_name` (`job`) but compared it with `organization` and `person`. Validation now checks the actual constraint names, matching the PostgreSQL/MySQL migration scripts.
- `tdb -u` now opens once without upgrade first; current databases skip confirmation, while only the recognized v1 upgrade case prompts and retries with `upgrade=True`.
- `tdb` now catches database initialization/migration exceptions at the callback boundary and reports `error: <message>` with exit code 1 instead of rendering a traceback. Typer's own invalid-option errors remain untouched.
- Database failures now raise `typer.BadParameter`, producing the same boxed `Error` panel as invalid options, e.g. `Invalid value: not a test_db file`.
- Fixed the partial-migration lockout: each engine's `upgrade_*_remove_encryption.sql` now performs both the job-cascade and encryption-removal changes before recording version 2, and the controller runs only that complete script.
- Fixed the broad CLI catch: expected `ValueError` and SQLObject `DatabaseError` exceptions remain boxed, while unexpected exceptions retain Typer's developer diagnostics. Added a regression test for this distinction.
- Added `tests/migrations/test_database_upgrade.py` under the `migration` marker. It uses `PYTEST_MIGRATION_DATABASE_CONNECTION_URI`, prepares a disposable v1 state for each backend, and verifies the real v1→v2 controller path; SQLite passed locally, while PostgreSQL/MySQL require disposable services.
- Hardened the migration test with an explicit `PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1` opt-in and an assertion that all `TestDB_EncryptedPickleCol%` metadata rows are removed.

## Schema-Tracking Recommendation

- Keep the linear version number for deciding which migration to run.
- Replace or supplement the mutable key with a `test_db_schema_migration` table containing migration version, identifier, and applied timestamp; record version 2 only after the complete migration succeeds.
- Validate a short set of invariants after migration (required tables/columns, removed encryption table, and engine-appropriate job foreign-key cascade), rather than hashing the entire schema across all three engines.
- Treat unknown versions, missing migration records, and failed invariants as refusal conditions. Do not attempt to infer or repair arbitrary manual schema edits.
