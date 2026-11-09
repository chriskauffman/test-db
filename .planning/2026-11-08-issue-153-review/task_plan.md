# Task Plan: Review issue #153 removal of encryption

## Goal
Remove the obsolete encryption settings and documentation identified in the issue #153 review, then verify the repository.

## Next Step
None; the requested test reorganization is complete.

## Current Phase
Phase 19

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints
- [x] Document in findings.md
- **Status:** complete

### Phase 2: Connected code review
- [x] Read the branch diff and callers
- [x] Check compatibility, docs, config, exports, and tests
- **Status:** complete

### Phase 3: Findings
- [x] Confirm each finding against current line numbers
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Run `make build`
- [x] Document test results
- **Status:** complete

### Phase 5: Delivery
- [x] Review outputs
- [x] Deliver to user
- **Status:** complete

### Phase 6: Implement the fix
- [x] Remove dead encryption settings and callers
- [x] Remove stale encryption documentation and config examples
- [x] Update affected tests and fixtures
- **Status:** complete

### Phase 7: Verify the fix
- [x] Run `make build`
- [x] Inspect the final diff and status
- **Status:** complete

### Phase 8: Add database migrations
- [x] Add SQLite, PostgreSQL, and MySQL migration scripts
- [x] Verify the scripts remove only the obsolete encryption objects
- **Status:** complete

### Phase 9: Bump application schema version
- [x] Set the current application schema version to 2
- [x] Update migration scripts and generated test fixture metadata
- [x] Run `make build`
- **Status:** complete

### Phase 10: Plan automatic v1-to-v2 upgrades
- [x] Make `DatabaseController._upgrade()` dispatch the complete v1-to-v2 migration for the active database engine
- [x] Apply both recent schema changes: job foreign-key cascades and encryption-surface removal
- [x] Set `TestDB_ApplicationSchemaVersion` to 2 only after the migration succeeds, then revalidate
- [x] Add explicit confirmation before the Typer CLI passes `upgrade=True`
- [x] Keep `tdb-console` upgrade-free so invalid databases are refused
- [x] Add tests for confirmation refusal, confirmation acceptance, migration execution, and version validation
- **Status:** complete

### Phase 11: Fix PostgreSQL post-upgrade validation
- [x] Correct PostgreSQL/MySQL invariant checks to validate constraint names
- [x] Verify the fix with targeted tests and `make build`
- **Status:** complete

### Phase 12: Confirm only required upgrades
- [x] Preflight the database without upgrading
- [x] Prompt only when the database reports a supported v1 upgrade
- [x] Test current, upgrade-required, and declined-confirmation paths
- [x] Run `make build`
- **Status:** complete

### Phase 13: Report database errors cleanly
- [x] Catch database initialization failures at the Typer boundary
- [x] Preserve parser errors and confirmation abort behavior
- [x] Add concise error-output coverage and run `make build`
- **Status:** complete

### Phase 14: Match boxed CLI error formatting
- [x] Raise Typer's supported parameter error type for database failures
- [x] Verify database errors render in the same boxed format as invalid options
- [x] Run `make build`
- **Status:** complete

### Phase 15: Make v1-to-v2 migration atomic by scope
- [x] Make each engine-specific v1-to-v2 SQL script include both schema changes
- [x] Make the controller execute one complete migration per engine
- [x] Verify standalone and controller SQLite upgrades
- **Status:** complete

### Phase 16: Preserve unexpected CLI diagnostics
- [x] Box expected `ValueError` and SQLObject database errors
- [x] Let unexpected runtime errors retain Typer developer diagnostics
- [x] Add regression coverage and run `make build`
- **Status:** complete

### Phase 17: Add marked migration tests
- [x] Add a separate `migration` pytest marker and disposable URI
- [x] Prepare v1 state for SQLite, PostgreSQL, and MySQL/MariaDB
- [x] Verify controller migration and schema invariants
- [x] Run the marked SQLite test and the normal build
- **Status:** complete

### Phase 18: Harden migration test safety and assertions
- [x] Require explicit destructive-test opt-in
- [x] Assert all encryption metadata is removed
- [x] Verify marked and normal test behavior
- **Status:** complete

### Phase 19: Separate CLI test suites
- [x] Move tdb-only key-value tests under `tests/cli/tdb`
- [x] Split lookup coverage between `tdb` and `tdb_console`
- [x] Run affected tests and `make build`
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Review branch `FEAT/issue-153-breaking-change-remove-encryption` against `main` | The current branch has one commit, `5b189c4`, referencing issue #153. |
| Do not edit product code | User asked for a review only. |
| Implement finding 1 after user approval | Remove the misleading encryption surface end-to-end. |
| Use standalone upgrade scripts | Existing schema upgrades are engine-specific SQL files; automatic schema migration is not wired into the controller. |
| Put confirmation in the CLIs | The controller should perform an already-authorized migration; CLI users must explicitly accept destructive test-data loss before `upgrade=True` is passed. |
| Keep migration ownership in `DatabaseController` | Both CLI entry points should share one versioned migration path and one post-migration schema check. |
| Treat v1 to v2 as one complete migration | Version 2 must represent both job cascade behavior and removal of obsolete encryption objects; partial upgrades must not be reported as complete. |
| Keep upgrades exclusive to `tdb` | The interactive console should never silently migrate or destroy data; it should refuse any database whose schema version is not current. |
| Keep a versioned migration cursor, but separate it from structural validation | Versioned migrations are portable and deterministic; a dedicated migration ledger and post-migration invariants are stronger than one mutable `KeyValue` row alone. |
| Validate PostgreSQL/MySQL cascades by constraint name | `information_schema.referential_constraints` does not provide the referenced table as `table_name`; the previous check compared `job` against `organization`/`person` and falsely rejected successful upgrades. |
| Preflight before confirmation | A current database should not require a destructive confirmation merely because `-u` was supplied; only the known v1 upgrade error triggers the prompt. |
| Render database failures as CLI errors | Database exceptions are user-facing operational errors, not programming tracebacks; print a concise message and exit 1 while leaving Typer parser diagnostics unchanged. |
| Use `typer.BadParameter` for boxed formatting | This Typer version formats its bundled Click exception types; importing the external `click.ClickException` bypassed that handler and produced a traceback. |
| Catch only known database failures | Unexpected runtime errors should not be mislabeled as invalid input; they should retain their developer traceback for diagnosis. |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| `make build` could not acquire the sandboxed uv cache lock | Re-ran the required command with approved elevated access; all checks passed. |
