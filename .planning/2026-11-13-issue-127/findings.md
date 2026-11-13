# Findings & Decisions

## Requirements
- Issue #127: collapse duplicated connection/no-connection branches in create signals.
- Pass `connection=kwargs.get("connection")` directly because SQLObject treats `None` as the default connection.
- User requested issue review and creation of a new branch.

## Research Findings
- Retrieved issue #127 successfully with `gh`.
- The issue identifies 11 repeated branches across `_person.py`, `_person_debit_card.py`, `_person_bank_account.py`, and `_organization*.py`.
- The repository is on clean `main` at `origin/main` before branch creation.
- Existing model tests use explicit connections; they did not cover `defaultConnection=True` with model constructors omitting `connection`.
- Added coverage that creates `Person` and `Organization` without explicit connections and verifies all five dependent model types are created.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| No helper or abstraction | Each replacement is a small direct simplification and the existing query calls already provide the right boundary |
| No new test fixture planned | Existing model and create-signal tests exercise these paths; verification will run the focused suite and full build |
| Use one isolated default-connection regression test | Root model creation triggers the affected address, bank-account, and debit-card signals while keeping setup small |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-
