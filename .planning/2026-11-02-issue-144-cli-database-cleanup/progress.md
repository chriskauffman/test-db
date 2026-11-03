# Progress Log

## Session: 2026-11-02

### Current Status
- **Phase:** 5 - Delivery
- **Started:** 2026-11-02

### Actions Taken
- Read issue 144 and confirmed the requested lifecycle cleanup.
- Created branch `fix/144-cli-database-cleanup` from `main`.
- Initialized this issue-specific planning directory.
- Inspected Typer's callback flow and confirmed `Context.call_on_close` is the command-lifetime cleanup hook.
- Registered `DatabaseController.close` with the callback context.
- Added a real Typer invocation regression test.
- Fixed shared SQLObject adapter cleanup so embedded callers remain usable.
- Added regression coverage for closing a controller backed by a preexisting cached adapter.
- Reviewed the connected code and final diff with Ponytail.

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| `tests/cli/tdb/test_tdb.py tests/cli/test_key_value_decryption_errors.py -q` | Pass | 8 passed; 1 known issue 136 warning | Pass |
| `tests/cli/tdb/test_tdb.py tests/cli/test_key_value_add_duplicate.py tests/cli/test_key_value_lookup.py tests/test_database_controller.py -q` | Pass | 57 passed | Pass |
| `make build` | Pass | 289 passed; lint, docs, type check, audit, and package build passed | Pass |

### Errors
| Error | Resolution |
|-------|------------|
| Initial full test run found 12 shared-connection failures | Preserved shared process connections and released only per-controller resources. |
| Initial cleanup retry found a double-close teardown error | Deleted raw resource references after release to make `close()` idempotent. |
