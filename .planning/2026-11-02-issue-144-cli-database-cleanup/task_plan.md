# Task Plan: GitHub Issue 144

## Goal
Close the database controller created for each Typer CLI command when the command finishes, including failures.

## Next Step
Hand the uncommitted issue 144 branch to the user for review.

## Current Phase
Phase 5

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints
- [x] Document in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define approach
- [x] Confirm the existing callback is the shared cleanup point
- **Status:** complete

### Phase 3: Implementation
- [x] Keep the controller in a local variable for command lifetime
- [x] Register cleanup at command completion with Typer's close hook
- [x] Add regression coverage
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Run focused CLI tests (8 passed)
- [x] Run `make build` (289 passed; audit and package build passed)
- **Status:** complete

### Phase 5: Delivery
- [x] Review the diff with Ponytail
- [x] Leave changes ready for user review
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Errors Encountered
| Error | Resolution |
|-------|------------|
| CLI cleanup closed a shared SQLObject adapter | Changed `DatabaseController.close()` to release controller-owned raw resources and close only adapters created by that controller; preserved shared process connections. |
| Full build type check rejected nullable resource attributes | Removed the `None` assignments and delete resource attributes after release instead. |
| Sandbox could not resolve the OSV audit service | Re-ran the unchanged build with network access; audit passed. |
