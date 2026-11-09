# Ponytail Audit — 2026-11-02

Scope: the whole repository. The audit assumed one operator or one CLI process at a time. Concurrent writers and live PostgreSQL/MySQL behavior were not exercised.

## Must fix

### 1. Failed database opens leak connections

Location: `src/test_db/_database_controller.py:101-129` and `:181-209`

`DatabaseController` opens a connection before validating the database, schema, and encryption key. Foreign databases, outdated schemas, wrong keys, and failed migrations raise without closing the connection.

Fix: wrap initialization in cleanup-on-error logic and clear `sqlhub.processConnection` when needed.

Impact: repeated failed opens leak SQLite connections and cursors, especially in tests and long-running processes.

### 2. Encrypted-row failures leave SQLObject iterators open

Location: `src/test_db/_encrypted_pickle_col.py:23-30`; related to issue #136.

Invalid encrypted data can raise while SQLObject 3.14.0 materializes a lazy query row. SQLObject does not clean up its `Iteration` cursor when row conversion raises, so a later database close reports `Cannot operate on a closed database`.

Fix: prefer an upstream SQLObject fix; otherwise add a narrow compatibility cleanup or pin a fixed release.

Impact: corrupt or mixed-key data produces pytest warnings and can become failures when warnings are treated as errors.

## Should fix

### 3. The Typer CLI never closes its database

Location: `src/test_db/tdb.py:110-112`

The callback creates a `DatabaseController` and discards the reference. The connection remains open until garbage collection or process exit.

Fix: keep the controller for the command lifetime and close it in a `finally` block.

Impact: embedded callers and tests can accumulate open connections and resource warnings.

### 4. One bad encrypted value stops an entire list

Location: `src/test_db/_views/_key_value.py:37-41`

The exception handler surrounds the whole loop. If one secure key-value cannot decrypt, later valid values are never displayed.

Fix: catch decryption errors per item, report the error, and continue.

Impact: one damaged row hides unrelated healthy data.

### 5. Importing CLI settings mutates the user’s home directory

Location: `src/test_db/_cli_settings.py:15-33`

Importing the settings module creates directories and touches a database and config file. Even help/version commands or imports can write to disk and fail under a read-only home.

Fix: move creation into CLI startup or a lazy settings initializer.

Impact: read-only commands have surprising side effects.

### 6. The README programmatic example does not work

Location: `README.md:169-183`

The example sets `test_db.connection_string`, which the package does not use, and passes `emailAddress` and `taxId`, which do not match model fields.

Fix: show `DatabaseController("sqlite:testdb.sqlite")`, pass its connection to models, and use `email` and `employerIdentificationNumber`.

Impact: new users copying the example get runtime errors immediately.
