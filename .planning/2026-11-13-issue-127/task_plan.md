# Task Plan: Implement issue #127

## Goal
Collapse the 11 duplicated connection/no-connection branches and cover both explicit and default SQLObject connections.

## Next Step
Review the final diff and hand off the completed change.

## Current Phase
Phase 6

## Phases

### Phase 1: Requirements & Discovery
- [ ] Understand user intent
- [x] Identify constraints
- [x] Document in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define approach
- [x] Create project structure
- **Status:** complete

### Phase 3: Implementation
- [x] Execute the plan
- [x] Write to files before executing
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Verify requirements met
- [x] Document test results
- **Status:** complete

### Phase 5: Delivery
- [x] Review outputs
- [x] Deliver to user
- **Status:** complete

### Phase 6: Default Connection Coverage
- [x] Add a regression test with `defaultConnection=True`
- [x] Create relevant models without explicit connections
- [x] Verify dependent create signals and restore global state
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Pass `connection=kwargs.get("connection")` to the existing query call | SQLObject treats `connection=None` as the default connection, eliminating duplicate branches without changing behavior |
| Keep the change limited to existing create-signal handlers | Issue #127 asks for deduplication; no new abstraction or dependency is needed |

## Planned Changes
- Inspect all 11 duplicated branches across person, debit-card, bank-account, organization, and address create-signal handlers.
- Replace each `if kwargs.get("connection")` / `else` pair with one call carrying the optional connection.
- Reuse the existing query methods and preserve their arguments, uniqueness loops, and error handling.
- Run focused tests for affected models, then `make build`.
- Add default-connection coverage in `tests/test_database_controller.py`.

## Errors Encountered
| Error | Resolution |
|-------|------------|
