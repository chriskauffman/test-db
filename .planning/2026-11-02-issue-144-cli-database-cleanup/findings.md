# Findings & Decisions

## Requirements
- Keep the `DatabaseController` created by the Typer callback alive for the command.
- Close it whether the command succeeds or raises.
- Preserve the existing unrelated audit report and generated fixture changes.

## Research Findings
- Issue 144 points to `src/test_db/tdb.py:110-112`, where the callback currently discards the controller reference.
- The callback is the shared setup point for the CLI commands, so cleanup belongs around the command yield rather than in each command.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Use a `try`/`finally` around the Typer callback yield. | It covers normal completion and command failures with no per-command duplication. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-
