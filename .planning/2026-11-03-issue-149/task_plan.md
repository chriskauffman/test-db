# Task Plan: Issue 149 — Avoid filesystem writes when importing CLI settings

## Goal
Importing `test_db._cli_settings` performs no filesystem writes; CLI startup still initializes required paths and files, with regression coverage and a passing build.

## Next Step
Run targeted tests for help/version side effects, then run `make build`.

## Current Phase
Phase 1

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
- [x] Review outputs
- [x] Deliver to user
- **Status:** complete

### Phase 6: Review Finding Fix
- [x] Move initialization after command selection
- [x] Cover help and version commands
- **Status:** complete

### Phase 7: Console Version Review Fix
- [x] Add early standalone console version handling
- [x] Add regression coverage
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Treat GitHub issue 149 as the source of truth | Jira was unavailable; the repository remote and user confirmed `gh` access. |
| Preserve existing working-tree changes | They predate this task and are unrelated. |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| Local branch creation was denied writing `.git/refs` in the sandbox | Request escalated permission for `git switch -c`. |
| `uv` could not create a lock temporary file in the shared cache | Retry verification with approved elevated access. |
| Existing close-handler test used `version`, which now intentionally skips database startup | Converted it to a direct callback test and kept separate version side-effect coverage. |
| `make build` schema fixture recipe used `version`, so the database was not created | Changed the recipe to run `person list`, a real database command. |
