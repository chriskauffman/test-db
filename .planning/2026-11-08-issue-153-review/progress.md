# Progress Log

## Session: 2026-11-08

### Current Status
- **Phase:** 1 - Requirements & Discovery
- **Started:** 2026-11-08

### Actions Taken
- Loaded repository guidance and review skills.
- Reviewed the branch commit and traced removed types through exports, ORM models, CLI, console, schema, tests, docs, and configuration.
- Confirmed the runtime no longer encrypts values while user-facing encryption settings and documentation remain.
- Ran `make build`; all checks passed.
- Removed the obsolete encryption settings, global options, controller argument, config examples, documentation, and related test fixture setup.
- Re-ran `make build`: 231 tests passed and all checks, audit, and package build passed.
- Reviewed upgrade flag wiring: the Typer CLI forwards `--upgrade/-u`; the console does not expose it; controller upgrade execution remains unimplemented.
- Bumped `CURRENT_APPLICATION_SCHEMA_VERSION` to 2 and updated all issue #153 migrations to write version 2.
- `make build` passed after the version bump: 231 tests, lint, type checks, audit, and package build; the generated SQLite fixture now contains schema version 2.
- Planned automatic v1→v2 upgrades with CLI confirmation: shared controller migration dispatch, complete job-cascade plus encryption-removal migration, version update last, and tests for accept/decline behavior.
- Adjusted the plan so only `tdb` can authorize upgrades; `tdb-console` remains upgrade-free and refuses invalid schema versions.
- Evaluated schema tracking: retain a versioned migration cursor, but consider a dedicated migration ledger plus post-migration structural invariants instead of relying on one mutable metadata key as validation.
- Implemented Phase 10: automatic v1→v2 migration dispatch, structural validation, Typer confirmation, and SQLite/controller/CLI tests.
- Fixed the PostgreSQL/MySQL cascade invariant query and reran verification: 234 tests passed with the current v2 schema target.
- Added conditional upgrade confirmation and reran verification: 235 tests passed with the current v2 schema target.
- Added clean database-error reporting and reran verification: 236 tests passed with the current v2 schema target.
- Matched Typer's boxed error formatting for database failures and reran verification: 236 tests passed.
- Fixed finding 1 by making each v1→v2 migration self-contained; standalone SQLite and controller upgrades passed, followed by `make build` with 236 passing tests.
- Fixed finding 3 by narrowing CLI exception handling and reran `make build`: 237 tests passed.
- Added marked migration coverage with a separate disposable database URI. SQLite migration passed; the default build reports 237 passed and 1 skipped migration test.
- Fixed migration-test safety and coverage gaps; opted-in SQLite migration passed and normal `make build` passed with 237 tests and 1 skipped migration test.
- Separated tdb-only key-value tests into `tests/cli/tdb` and split lookup coverage into distinct tdb and tdb-console modules. Affected tests passed: 27; `make build` passed with 237 tests and 1 skipped migration test.

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| SQLite encryption-removal migration | Remove legacy table and metadata, retain unrelated key values | Table count `0`; only `keep` metadata row remained | Passed |
| SQLite legacy v1 migration | Set application schema version to 2 and remove obsolete objects | Version `2`; obsolete table and metadata counts `0` | Passed |
| `make build` | All repository checks pass | 234 tests passed; lint, type check, audit, and build passed | Passed |

### Errors
| Error | Resolution |
|-------|------------|
| GitHub issue page/API unavailable | Reviewed local issue branch and commit scope. |
| uv cache permission failure in sandbox | Re-ran `make build` with approved elevated access. |
| SQLite legacy schema fixture creates reserved `sqlite_sequence` table on current SQLite | Omitted that legacy fixture line for the execution check; SQLite created the internal table automatically. |
