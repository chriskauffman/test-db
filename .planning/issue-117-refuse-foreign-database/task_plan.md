# Task Plan: Issue #117 — Refuse to initialise a foreign database

## Goal

`DatabaseController` must only create its schema in a database with no tables. Any other non-test_db database raises `ValueError("not a test_db file")` and is left untouched.

## Phases

- Phase 1: Discovery — `_isEmptyDB` only checked for missing `TestDB_Application*` rows, so any database without a `key_value` table looked empty. **complete**
- Phase 2: Implement — `_isEmptyDB` now returns `not connection.listTables()` (supported by SQLite, PostgreSQL and MySQL SQLObject backends); fix stale `autoCreate=True` docstring. **complete**
- Phase 3: Test — add `test_open_foreign_database_refused`. **complete**
- Phase 4: Verify — `make build`. **in progress**
