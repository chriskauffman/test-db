# Findings & Decisions

## Requirements
- Review all currently open issues in `chriskauffman/test-db` and classify whether each remains valid against the current repository and associated PR history.

## Research Findings
- GitHub currently reports 10 open issues: #158, #157, #148, #147, #146, #136, #130, #129, #128, #127.
- The local checkout is on `main` at `origin/main`; the worktree is clean apart from this review plan.
- Open issue bodies are mostly audit findings from 2026-10-31/2026-11-02, plus feature issues #157 and #158.
- PR #159 merged the #158 implementation; #158 remains open because the merged release PR reference is still open and the implementation PR used `Refs #158`.
- PR #160 merged the MariaDB migration-test fix; no open issue is attached to that change.
- The current README programmatic example still uses the invalid `test_db.connection_string`, `emailAddress`, and `taxId` names, so #148 is valid.
- Current console commands still use the `tdb_` prefix, so #157 is valid.
- `KeyValueView.list` still has no per-row error handling, so #147 matches current code, but the supported encryption implementation was removed in schema v2.
- `_encrypted_pickle_col.py`, `EncryptedPickleValidator`, and secure key-value model code are absent from current `main`; #130, #136, and #146 refer to removed code and are stale/invalid for this release.
- Current models still contain duplicated `_set_gID` methods (#128), duplicated connection/no-connection branches (#127), and `_TyperOptions` (#129), so all three remain valid cleanup issues.

## Issue Classification
| Issue | Status | Evidence / recommendation |
|-------|--------|---------------------------|
| [#158](https://github.com/chriskauffman/test-db/issues/158) | Resolved, administratively open | PR #159 merged the implementation; close the issue. |
| [#157](https://github.com/chriskauffman/test-db/issues/157) | Valid | `src/test_db/console/` still defines `tdb_...` commands. |
| [#148](https://github.com/chriskauffman/test-db/issues/148) | Valid | README example still uses nonexistent settings and model field names. |
| [#147](https://github.com/chriskauffman/test-db/issues/147) | Stale / superseded | Encryption support was removed by schema-v2 work; `KeyValueView` has no encrypted values to continue past. Close or rewrite against current behavior. |
| [#146](https://github.com/chriskauffman/test-db/issues/146) | Stale / superseded | The referenced encrypted row-conversion code no longer exists. Close. |
| [#136](https://github.com/chriskauffman/test-db/issues/136) | Stale / superseded | The warning’s encrypted iterator path was removed; current code no longer reproduces the described path. Close. |
| [#130](https://github.com/chriskauffman/test-db/issues/130) | Invalid | `EncryptedPickleValidator` and its file are gone. Close. |
| [#129](https://github.com/chriskauffman/test-db/issues/129) | Valid | `_TyperOptions` remains and is still imported by CLI commands. |
| [#128](https://github.com/chriskauffman/test-db/issues/128) | Valid | Multiple model classes still duplicate `_set_gID`. |
| [#127](https://github.com/chriskauffman/test-db/issues/127) | Valid | Multiple create signal handlers still duplicate connection branches. |

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| `gh issue view --json closedByPullRequests` rejected the field | Use supported `closedByPullRequestsReferences` field. |

## Resources
-
