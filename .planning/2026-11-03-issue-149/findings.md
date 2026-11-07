# Findings & Decisions

## Requirements
- GitHub issue 149: importing `src/test_db/_cli_settings.py` currently creates directories and touches a database/config file.
- Help/version commands and imports must not write to disk or fail under a read-only home.
- Move creation into CLI startup or a lazy settings initializer.
- URL: https://github.com/chriskauffman/test-db/issues/149

## Research Findings
- `tdb-console version quit` is passed as command-line arguments and is used by the Makefile command test.
- `tdb_console.main()` currently initializes paths, logging, history, and the database before cmd2 processes those arguments.
- The smallest compatible fix is to handle the standalone `version` and `version quit` argument forms before normal console startup.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Jira/TWG lookup failed with `api.atlassian.com` DNS error | Used the repository GitHub issue after user authorized `gh`. |

## Resources
-
