# Task Plan: Issue #101 — Persist Encryption Iteration Settings

Use this file as the durable roadmap for the task. Create it before complex work and keep it current as phases change.

## Goal

Keep encrypted values readable with the same password after runtime iteration settings change by persisting the PBKDF2 iteration count alongside the salt.

## Next Step

Completed implementation, make build, and final Ponytail review. Deliver the verified changes without committing.

## Current Phase

Phase 5: Delivery

## Phases

### Phase 1: Requirements & Discovery

- Read issue #101 and trace salt persistence, iteration configuration, encrypted columns, and test fixtures.
- Record findings in findings.md.
- **Status:** complete

### Phase 2: Planning & Structure

- Establish this selected task directory without modifying archived plans.
- Complete Ponytail review and record restricted-key protection and partial-metadata handling.
- Selected authenticated migration on the user's implementation request; verify a raw ciphertext sample before persisting legacy counts.
- Finalized empty/null-only handling: no ciphertext exists to lock out, so use the validated configured count.
- **Status:** complete

### Phase 3: Implementation

- Reproduce the setting-change failure in a focused regression test.
- Persist and reuse a validated positive iteration count in DatabaseController.
- Add the iteration key to the existing RESTRICTED_KEYS list.
- Reject iterations-without-salt corruption without regenerating metadata.
- Implement only the approved legacy migration policy; do not silently backfill an unverified count.
- Document new-database and legacy behavior.
- **Status:** complete

### Phase 4: Testing & Verification

- Test metadata persistence, changed settings, the approved legacy policy, malformed/partial metadata, wrong passwords, and absent encryption keys.
- Verify CLI and console reject edit/delete of the new restricted key.
- Include legacy wrong-count-first-open behavior and assert failed validation does not rewrite encryption metadata.
- Avoid ORM caching masking failures by checking actual ciphertext decryption.
- Run focused tests and make build; record outcomes and blockers.
- **Status:** complete

### Phase 5: Delivery

- Review the diff using Ponytail's smallest-complete-change guidance.
- Update planning records and report verification results.
- Leave changes uncommitted unless explicitly requested.
- **Status:** complete

## Key Questions

1. Is a schema migration required? No: use an additional KeyValue record.
2. Can the historical count be recovered from the salt or ciphertext? No. Legacy first-open backfill requires the original configured count.
3. Does Fernet construction alone authenticate a password/count? No. The implementation explicitly decrypts one raw legacy ciphertext sample before backfilling. Complete metadata continues authenticating on ciphertext reads; no sample is needed when no non-null encrypted values exist.
4. Should current settings replace existing metadata? No: persisted settings take precedence; malformed metadata must fail clearly.
5. Is blind legacy backfill safe? No: an incorrect first-open setting would become persisted before decryption and restoring configuration alone would no longer recover access.
6. Which legacy policy is selected? Authenticated migration. PersonSecureKeyValue.value is the only encrypted column. Select one non-null raw value using SQLObject, normalize its BLOB using BinaryValidator, and Fernet.decrypt without unpickling before saving the count. Empty/null-only databases can safely adopt the configured count.

## Decisions Made

- Implemented metadata key: TestDB_EncryptedPickleColIterations, stored as a string alongside TestDB_EncryptedPickleColSalt.
- Preserve the existing salt encoding, password handling, cipher, and schema version.
- Reuse RESTRICTED_KEYS for CLI/console edit/delete protection; do not duplicate guards.
- Validate fresh configured counts before writing encryption metadata and reject incomplete metadata without generating a replacement salt.
- No-key initialization must leave encryption metadata untouched.
- Use small focused tests, independent legacy fixtures, cache-independent decryption, and monkeypatch restoration of globals.
- Avoid new dependencies, arbitrary iteration limits, a settings framework, or unrelated encryption changes.
- The original automatic legacy backfill proposal is superseded by authenticated migration. On authentication failure, leave encryption metadata unchanged and allow retry with the original password/count.
- Probe one encrypted sample rather than scanning all records; existing mixed-key/corrupt datasets are outside this fix.
- Work directly in this worktree; no child agents are needed for this tightly coupled change.
- Selected planning directory: .planning/issue-101-encryption-settings-not-stored/.
- Native helpers were not found in the standard local skill directories checked. Use the upstream template structure as a fallback; native initialization and validation are unavailable.

## Errors Encountered

- Attempt 1: ~/.agents/skills and ~/.claude/skills do not exist; read upstream skill guidance and templates directly instead.
- No ponytail executable was found on PATH; read upstream Ponytail guidance directly.
- Implementation research attempt 1: SQLObjectState is not exported by sqlobject.main; use standard-library SimpleNamespace to supply the existing BinaryValidator connection state instead.
- Regression-first run: test_reopen_uses_persisted_iterations failed as expected with InvalidToken after changing the configured count.
- First focused implementation run: 20 passed, 7 failed. SQLObject exposes ISNOTNULL rather than ISNOT; console main raises SystemExit(0) normally. Corrected the predicate and test expectations.
- An edit patch failed after Ruff changed its expected whitespace; re-read the affected file and reapplied with matching context.
- Second focused run: all 27 tests passed and ty passed. Ruff flagged the deliberate failing property access in a test; assigned it to _ to preserve the assertion without B018.
- Final make build: passed all checks and 210 tests; uv audit reported no known vulnerabilities or adverse statuses in 45 packages. Wheel and source distribution built successfully.
- Build emitted nonblocking warnings for experimental uv audit and uv/uv-build version range; no dependency or build configuration changes were needed.
- make build regenerated the tracked tests/data/test_schema_v1.sqlite binary. Restored only that generated change after confirming src/test_db/_schemas/v1.sql was unchanged.

## Notes

- Update phase status as work progresses: pending to in_progress to complete.
- Re-read the goal and next step before major decisions.
- Log errors promptly so failed approaches are not repeated.
- Implementation plan artifact: ebc8b8fb-a282-4145-9145-321d0a2e70b9.
- Final Ponytail review: reused existing SQLObject conversion and restricted-key guards; no schema changes, new dependencies, re-encryption feature, or unrelated refactoring.
- Live PostgreSQL/MySQL integration was not run. The new controller regressions use temporary SQLite databases; backend BLOB conversion reuses SQLObject's existing BinaryValidator.
