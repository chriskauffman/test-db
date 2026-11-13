# Findings & Decisions

## Requirements
- Issue #127: collapse duplicated connection/no-connection branches in create signals.
- Pass `connection=kwargs.get("connection")` directly because SQLObject treats `None` as the default connection.
- User requested issue review and creation of a new branch.

## Research Findings
- Retrieved issue #127 successfully with `gh`.
- The issue identifies 11 repeated branches across `_person.py`, `_person_debit_card.py`, `_person_bank_account.py`, and `_organization*.py`.
- The repository is on clean `main` at `origin/main` before branch creation.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| No helper or abstraction | Each replacement is a small direct simplification and the existing query calls already provide the right boundary |
| No new test fixture planned | Existing model and create-signal tests exercise these paths; verification will run the focused suite and full build |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-
