# Task Plan: Issue #104 — SQLite Foreign-Key Enforcement

Use this file as the durable roadmap for the task. Create it before complex work and keep it current as phases change.

## Goal

Reject orphan relationships through SQLObject by enabling foreign-key enforcement on every SQLite physical connection used by DatabaseController.

## Next Step

Deliver the verified, uncommitted changes for issue #104.

## Current Phase

Phase 5: Delivery

## Phases

### Phase 1: Requirements & Discovery

- Read issue #104, the controller, address model, existing tests, and installed SQLObject connection code.
- Record connection lifecycle and URI caching findings.
- **Status:** complete

### Phase 2: Planning & Structure

- Create the issue branch and isolated planning directory.
- Record the implementation plan and await user approval.
- User approved implementation after requesting a task-plan review.
- **Status:** complete

### Phase 3: Implementation

- Reproduce the ORM orphan-insert failure in a regression test.
- Confirm the smallest SQLite-only integration compatible with SQLObject URI caching and both connection creation paths.
- Enable foreign keys before physical connections are used; remove the late raw-only configuration.
- Preserve other backends and existing connection identity behavior.
- **Status:** complete

### Phase 4: Testing & Verification

- Cover raw/ORM enforcement, orphan rejection, valid and nullable relationships, fresh connections, reopening, and in-memory behavior.
- Run focused controller/address/memory tests and make build.
- Inspect generated fixtures and review cascade behavior under active constraints.
- **Status:** complete

### Phase 5: Delivery

- Review the complete diff using Ponytail guidance.
- Record validation outcomes and remaining limitations.
- Leave changes uncommitted unless explicitly requested.
- **Status:** complete

## Key Questions

1. Why does the current PRAGMA miss ORM operations? The controller retains one raw connection while SQLObject can create another for queries.
2. Are in-memory connections created through the same path? No: SQLObject also uses makeMemoryConnection, including when closing/recreating an in-memory connection.
3. Can a callable factory be passed directly to connectionForURI? Its keyword arguments are URL-encoded; do not assume direct callable support.
4. Which integration should be implemented? Preserve connectionForURI and configure the cached SQLite adapter's _connOptions factory with a sqlite3.Connection subclass. Enable the existing ORM connection once before acquiring the raw connection; future file and memory connections use the factory.
5. Is existing-data cleanup required? No; detecting or repairing historical orphan rows is outside #104.

## Decisions Made

- Branch: fix/issue-104-sqlite-foreign-key-enforcement, created from main.
- Planning directory: .planning/issue-104-sqlite-foreign-key-enforcement/.
- Preserve untracked PONYTAIL_REVIEW.md and all existing planning directories.
- No new dependencies, global SQLObject patch, schema change, or unrelated review fixes.
- No child agents: connection setup and its regression tests are a small, tightly coupled change.
- Preserve SQLObject's cached adapter: encryption tests directly clear and close connectionForURI(uri), so a separate adapter/cache would change existing behavior.
- SQLObject's internal _connOptions mapping is the narrow integration point for a callable DB-API factory; URI arguments serialize callables and are unsuitable.
- Native helpers were not found in the standard local skill directories checked. Use upstream template structure as fallback; native initialization and validation are unavailable.
- Implementation plan artifact: 59d7a128-3581-43d9-8e6c-dd30b91b1ebe.

## Errors Encountered

- Skill discovery attempt 1: ~/.agents/skills, ~/.claude/skills, and ~/.config/agents/skills do not exist. Read the upstream planning-with-files skill and templates directly.
- Research attempt 1: DBAPI has no makeConnection attribute; inspect the SQLiteConnection subclass and DBConnection initialization instead.
- Regression-first attempt 1: ORM PRAGMA returned (0,) while raw returned (1,). The orphan insert reached a post-create auto-dependent listener and raised SQLObjectNotFound instead of IntegrityError; disable autoCreateDependents with monkeypatch to isolate database enforcement.
- Regression-first attempt 2: both failures reproduced as intended: ORM PRAGMA (0,) and orphan insert did not raise IntegrityError.
- Implementation edit attempts 1–2: patch context mismatch; re-read affected files and applied separate exact-context edits.
- First focused implementation run: 30 tests passed, but file inspection revealed trailing additions had not been retained by the edit. Inserted the missing regression functions with a following context anchor, then reran: all 41 focused tests and ty passed.
- make build passed: 221 tests, formatting/lint/docstring/YAML checks, ty, dependency audit (45 packages), and packaging.
- Build emitted nonblocking warnings for experimental uv audit and uv/uv-build version range.
- Restored only the generated tests/data/test_schema_v1.sqlite binary after verifying the schema source was unchanged. Confirmed the restored fixture's schema matches src/test_db/_schemas/v1.sql.

## Notes

- Update phase status as work progresses: pending to in_progress to complete.
- Re-read the goal and next step before major decisions.
- Log errors promptly so failed approaches are not repeated.
- Implementation and verification are complete. Final Ponytail review found no blockers for local CLI/API use.
- No schema/version changes, dependencies, or unrelated fixes; all changes remain uncommitted.
- Live PostgreSQL/MySQL and high-concurrency behavior were not tested. The factory integration intentionally uses SQLObject's internal _connOptions mapping; regression tests cover the installed dependency's lifecycle.
