# Task Plan: Issue #119 — Deleting a person or organization with jobs fails

## Goal

Deleting a person deletes their jobs (plus addresses, bank accounts, debit cards, key values, secure key values). Deleting an organization deletes its jobs. Decision confirmed by the owner in the issue comment.

## Design

- `Job.person` and `Job.organization` get `cascade=True`, like every other foreign key. SQLObject cascades in Python, so existing databases need no migration; deleting a job already cascades to its key values.

## Phases

- Discovery: Job foreign keys were the only ones without a cascade setting, so SQLite foreign-key enforcement (#104) made deletes fail. **complete**
- Implement: two-line change in `_job.py`. **complete**
- Tests: person delete (jobs and all dependents, other rows untouched) and organization delete (jobs and job key values). Both fail without the fix. **complete**
- Verify: `make build`, plus `tdb person delete` on a person created by `job add`. **in progress**
