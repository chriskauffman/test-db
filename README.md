# test-db

Python Test Database That Automatically Generates Test Data

A comprehensive tool for creating, managing, and seeding test databases with realistic data. Supports SQLite, PostgreSQL, and MySQL with an intuitive CLI and interactive console.

## Quick Start

### Installation

For SQLite (default):

```bash
uv tool install --python 3.14 git+ssh://git@github.com/chriskauffman/test-db.git
```

For PostgreSQL or MySQL support:

```bash
uv tool install --python 3.14 --with "psycopg[binary]" --with "mysqlclient" \
  git+ssh://git@github.com/chriskauffman/test-db.git
```

### Basic Usage

```bash
# View available commands
tdb --help

# Create a person in the database
tdb person add "John Doe" "john@example.com"

# List all people
tdb person list

# Interactive console
tdb-console
```

## Architecture Overview

### Project Structure

- **`src/test_db/`**: Core package
  - `_person.py`, `_organization.py`, `_job.py`: Data models
  - `_address.py`, `_bank_account.py`: Related entities
  - `_key_value.py`, `_type_id_col.py`: Utilities
  - `_database_controller.py`: Database initialization and management
  - `cli/`: Command-line interface using Typer
  - `console/`: Interactive console using cmd2
  - `_views/`: Display and formatting for database objects

- **`tests/`**: Comprehensive test suite
  - `cli/tdb/`: CLI command tests
  - `cli/tdb_console/`: Console command tests
  - Unit tests for core functionality

### Data Models

The tool manages the following primary entities:

- **Person**: Represents individuals with addresses, bank accounts, debit cards
- **Organization**: Represents companies with addresses and bank accounts
- **Job**: Employment records linking persons to organizations
- **KeyValue**: Generic key-value storage (with restricted system keys)
- **Address**: Address records for persons and organizations
- **BankAccount**: Bank account information
- **DebitCard**: Debit card records

### Key Features

- **Test Data Generation**: Uses Faker to generate realistic test data
- **Dual Interfaces**: CLI for scripting, interactive console for exploration
- **Type-Safe IDs**: TypeID support for distributed system compatibility
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL
- **Comprehensive Testing**: 181+ tests with 90%+ coverage

## Database Connections

test-db should support any valid [SQLObject connection](https://sqlobject.readthedocs.io/en/stable/SQLObject.html#declaring-a-connection).
SQLite connections opened through `DatabaseController` enable foreign-key checks,
including ORM queries and newly created physical connections. References to
nonexistent parents are rejected, and existing database-defined delete cascades
are enforced. Existing orphaned rows are not repaired automatically.

Pytest supports the connection environment variable `PYTEST_DATABASE_CONNECTION_URI`.
If this is set with a valid SQLObject connection URI such as:

- `export PYTEST_DATABASE_CONNECTION_URI=postgresql://user:pass@localhost/testdb`
- `export PYTEST_DATABASE_CONNECTION_URI=mysql://user:pass@localhost/testdb`

it will be used to execute tests when `uv run pytest` or `make` is executed. If it is unset, tests will run against a sqlite file.

Note: You must install database drivers to support the connection specified, such as `uv add "psycopg[binary]"` or `uv add mysqlclient`.

Migration tests are destructive and use a separate connection variable. Point
`PYTEST_MIGRATION_DATABASE_CONNECTION_URI` at a disposable database and set
`PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1`, then run
`uv run pytest -m migration tests/migrations`.

### Protecting Credentials & Standard Config Files

`test-db` protects sensitive database credentials by handling connection strings as `SecretStr` objects, masking credentials in debug logs, error dumps, and console outputs.

To adhere to security best practices and keep credentials out of connection strings, command history, and environment variables entirely, use standard database authentication files:

- **PostgreSQL (`~/.pgpass`)**:
  Store credentials in `~/.pgpass` (`chmod 0600 ~/.pgpass`):
  ```
  localhost:5432:testdb:myuser:mypassword
  ```
  Then connect with a passwordless URI:
  ```bash
  export DB_CONNECTION_URI="postgresql://myuser@localhost:5432/testdb"
  ```
- **MySQL / MariaDB (`~/.my.cnf`)**:
  Store credentials in `~/.my.cnf` (`chmod 0600 ~/.my.cnf`):
  ```ini
  [client]
  user=myuser
  password=mypassword
  host=localhost
  ```
  Then connect with a passwordless URI:
  ```bash
  export DB_CONNECTION_URI="mysql://myuser@localhost:3306/testdb"
  ```

### Data protection

test-db stores test data without encryption. Applications that need encrypted
storage should encrypt data before giving it to test-db or use an application-
owned encrypted storage layer.

### Execution directly without install

Run commands without installation:

```bash
uvx --from git+ssh://git@github.com/chriskauffman/test-db.git --python 3.14 tdb job list

uvx --from git+ssh://git@github.com/chriskauffman/test-db.git --with "psycopg[binary]" \
  --python 3.14 tdb -d postgresql://user:pass@localhost/testdb job list
```

### Updating

```bash
uv tool upgrade test-db
```

## Programmatic Usage

You can also use test-db as a library in your own Python code:

```python
from test_db import DatabaseController, Job, Organization, Person

# Create a database connection
db = DatabaseController("sqlite:testdb.sqlite")

try:
    # Create a person
    person = Person(
        connection=db.connection,
        firstName="John",
        lastName="Doe",
        email="john@example.com",
    )

    # Create an organization
    org = Organization(
        connection=db.connection,
        name="Acme Corp",
        employerIdentificationNumber="12-3456789",
    )

    # Create a job entry
    job = Job(connection=db.connection, person=person, organization=org)

    # Query data
    people = list(Person.select(connection=db.connection))
    for person in people:
        print(f"{person.firstName} {person.lastName}")

    # Access related data
    for person in people:
        for job in person.jobs:
            print(f"Works at {job.organization.name}")
finally:
    db.close()
```

### Replacing removed lookup helpers

Use SQLObject's native `selectBy` and relationship attributes instead of the
removed `byOrganizationAndPerson` and `getKeyValueByKey` helpers. Call
`getOne()` when the query is expected to return exactly one row:

```python
from test_db import Job, PersonKeyValue

# Replaces byOrganizationAndPerson
job = Job.selectBy(organization=org, person=person).getOne()

# Replaces getKeyValueByKey for a person
key_value = PersonKeyValue.selectBy(person=person, key="department").getOne()
```

If multiple rows are valid, omit `getOne()` and iterate the `SelectResults`
instead:

```python
jobs = Job.selectBy(organization=org, person=person)
for job in jobs:
    print(job.position)
```

Use `organization.keyValues` with `OrganizationKeyValue.selectBy(...)` or
`job.keyValues` with `JobKeyValue.selectBy(...)` for the corresponding
organization and job key/value records.

## Resetting Databases

For MariaDB:

```bash
mariadb -u root -h localhost -p < src/test_db/_schemas/reset_mysql.sql
```

For PostgreSQL:

```bash
psql -h localhost -U postgres -f src/test_db/_schemas/reset_postgresql.sql
```
