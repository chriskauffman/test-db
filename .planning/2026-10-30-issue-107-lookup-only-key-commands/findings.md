# Findings & Decisions

## Requirements
- Issue 107 requires missing-key view/delete to report an error without creating data in CLI and console commands.
- Scope: person, job, organization, and person secure keys; make build must pass.

## Research Findings
- Each CLI key module has view/delete calls to get-or-create. Console modules repeat the same behavior.
- Model helpers already demonstrate owner-scoped relationship filtering and getOne queries.
- CLI validation uses stderr and exit 1; BaseCommandSet validation uses console perror.
- Existing command tests exercise successful add/list/view/delete and use disposable SQLite via shared fixtures.
- Delete can insert then destroy a row, so a final row count alone cannot prove lookup-only behavior.
- Existing untracked PONYTAIL_REVIEW.md predates this task and must remain untouched.
- SQLObject SelectResults exposes sourceClass; filter(sourceClass.q.key == key).getOne() preserves the owner and connection already present in each relationship query.
- Tests wrap the model _create method to catch transient insert attempts without adding event listeners or changing underlying behavior.
- Final lookup implementation passes all 32 regression variants, including cross-owner cases; existing successful command coverage also passes.
- Existing model helpers and add/edit commands were left unchanged. Full build passes all 262 tests.

## Technical Decisions
- Preserve model get-or-create semantics and add/edit commands.
- Introduce lookup/error handling in existing validation surfaces, not a new model API or module.
- Cover cross-owner isolation in regressions.

## Issues Encountered
- Requested planning-with-files was not locally installed at checked paths; fetched upstream skill and inspected initialization helpers in a temporary directory.
- Downloaded skill is not registered with read_skill; read_files provided its instructions.

## Resources
- Issue: https://github.com/chriskauffman/test-db/issues/107
- Skill: https://github.com/othmanadi/planning-with-files
