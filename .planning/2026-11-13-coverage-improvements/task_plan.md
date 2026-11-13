# Task Plan: Improve test coverage

## Goal
Coverage improvements are developed on a dedicated branch, prioritizing skipped migrations and low-coverage interactive views.

## Next Step
Review the new view tests and coverage results.

## Current Phase
Phase 4

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
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
- [ ] Review outputs
- [ ] Deliver to user
- **Status:** pending

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Add focused unit tests for shared input helpers and representative view flows | Covers validation loops, edit/detail behavior, and deletion confirmation without duplicating console integration tests |

## Results
- Added `tests/test_views.py` with three focused tests.
- Coverage increased from 91% to 93%.
- View coverage improved materially; one migration test remains intentionally skipped without a disposable migration database.
- Added `src/test_db/_connection.py` to load the local MySQL client config for passwordless MySQL URIs.

## Errors Encountered
| Error | Resolution |
|-------|------------|
