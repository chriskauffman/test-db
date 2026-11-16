# Findings & Decisions

## Requirements
- Review the repository's GitHub Actions changes/workflows without changing code.
- Follow repository verification guidance where practical (`make build`).

## Research Findings
- The worktree and `chore/improve-ci` are identical to `main`; there are no uncommitted workflow changes.
- The latest workflow-related commit in the repository is `6ca9150`, which changed `uv pip audit` to `uv audit` in `.github/workflows/push.yml`.
- Current workflows are `publish.yml`, `push.yml`, and `release-please.yml`.
- `yamllint .github` passes.
- `make build` passes: 249 tests passed, 1 skipped; migration test passed; audit found no known vulnerabilities; build produced both distributions.
- `push.yml` filters pushes to source/config paths but omits `.github/workflows/**`, so a workflow-only change on `main` or `release/*` will not run this CI workflow.
- `push.yml` runs the full `make` target in all four Python matrix jobs and then runs the same full `make` target again in the `build` job after the matrix and security job complete.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Initial `make build` could not create a uv cache temp file in the sandbox | Retried with approved elevated filesystem access; build passed |
| `actionlint` is not installed | Used yamllint and repository build checks; recorded as not checked |
| `gh pr status` could not connect to GitHub | Reviewed local refs and workflow history instead |

## Resources
-
