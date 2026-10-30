# Task Plan: Issue 107 — lookup-only key view/delete commands

## Goal
View/delete commands report missing keys without inserting data across CLI and console person, job, organization, and person secure keys.

## Next Step
Await user direction; implementation and verification are complete, with no commit or push requested.

## Current Phase
All five phases complete.

## Phases

### Phase 1: Requirements & Discovery
Issue and all eight affected command modules inspected. Sixteen view/delete handlers use get-or-create helpers.
- **Status:** complete

### Phase 2: Planning & Structure
Use owner-scoped relationship lookups and existing validation surfaces for shared missing-key reporting. CLI exits 1; console reports an error and returns. Keep model helpers and add/edit behavior unchanged. The implementation plan is recorded in the conversation plan artifact titled “Issue 107: make key view/delete operations lookup-only.”
- **Status:** complete

### Phase 3: Implementation
After approval, add regressions, confirm failures, then update all affected handlers and remove obsolete TODOs.
- **Status:** complete

### Phase 4: Testing & Verification
Cover both operations, both interfaces, all four key types, and cross-owner isolation. Assert errors, row counts, and no insert attempt, including transient inserts during delete. Run affected suites and make build; record results.
- **Status:** complete

### Phase 5: Delivery
Perform Ponytail review and inspect the final diff. Restore only build-generated fixture changes. Keep changes local until asked to commit or push; preserve PONYTAIL_REVIEW.md.
- **Status:** complete

## Decisions Made
- Keep get-or-create library helpers: add/edit and existing callers intentionally use them.
- Reuse validation modules: consistent errors without repeating exception handling across 16 handlers.
- Work serially: shared helper contracts and repetitive changes do not justify child-agent coordination.
- Branch: fix/107-lookup-only-key-commands.
- Task directory: .planning/2026-10-30-issue-107-lookup-only-key-commands.

## Errors Encountered
- No planning skill installation was found in the checked local locations. Downloaded upstream skill and required helpers to /tmp/test-db-planning-with-files and inspected helpers before running the initializer.
- read_skill could not load the downloaded skill path; read the complete SKILL.md through read_files instead.
- SQLObject API inspection showed no removeListener or filterBy; used a scoped _create wrapper and sourceClass/filter instead.
- First implementation run found four console view edits had not applied; explicit handler-context patches fixed all eight failing variants.
