# Task Plan: Safer database upgrades

## Goal
Database upgrades remain available, but transactional backends roll back failures and MariaDB upgrades can resume after partial DDL progress.

## Next Step
Implement the runner and MariaDB retry logic, then add focused tests and run the build.

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [ ] Understand user intent
- [ ] Identify constraints
- [ ] Document in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [ ] Define approach
- [ ] Create project structure
- **Status:** complete

### Phase 3: Implementation
- [ ] Execute the plan
- [ ] Write to files before executing
- [x] Add explicit rollback and SQLite foreign-key recovery
- [x] Make MariaDB foreign-key migration steps retryable
- [x] Add focused retry coverage
- **Status:** complete

### Phase 4: Testing & Verification
- [ ] Verify requirements met
- [ ] Document test results
- [x] Targeted controller tests pass
- [x] Full `make build` passes
- **Status:** complete

### Phase 5: Delivery
- [ ] Review outputs
- [ ] Deliver to user
- [x] Review final diff and report external-backend test limitation
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Errors Encountered
| Error | Resolution |
|-------|------------|
