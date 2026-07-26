# Contributing to test-db

Thank you for your interest in contributing to test-db! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/chriskauffman/test-db.git
   cd test-db
   ```

2. Install development dependencies:
   ```bash
   make init
   ```

3. Verify setup with tests:
   ```bash
   make test
   ```

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes in the `src/test_db/` directory

3. Run tests locally:
   ```bash
   make test
   ```

4. Check code quality:
   ```bash
   make lint
   make type-check
   ```

5. Format code:
   ```bash
   make format
   ```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_example.py -v

# Run with coverage report
make coverage
```

### Code Quality Standards

- **Linting**: Ruff (automatic with `make lint`)
- **Type Checking**: `ty` (automatic with `make type-check`)
- **Documentation**: Google-style docstrings (checked with `pydoclint`)
- **YAML**: Validated with `yamllint`

The `make` command runs all checks: linting, type checking, tests, and builds.

## Project Structure

```
src/test_db/
├── _*.py              # Data models (person, organization, job, etc.)
├── _database_controller.py  # Database initialization
├── _cli_settings.py   # CLI configuration
├── cli/               # Typer-based CLI commands
├── console/           # cmd2-based interactive console
├── _views/            # Object display and formatting
├── _listeners.py      # Event listeners
├── tdb.py            # Main CLI entry point
└── tdb_console.py    # Console entry point

tests/
├── cli/
│   ├── tdb/          # CLI command tests
│   └── tdb_console/  # Console command tests
├── conftest.py       # Shared test fixtures
└── test_*.py         # Unit tests
```

## Adding Features

### Adding a New CLI Command

1. Create command function in `src/test_db/cli/_command_name.py`
2. Register it in `src/test_db/tdb.py`
3. Add tests in `tests/cli/tdb/test_tdb_command_name.py`

### Adding Console Commands

1. Create command set in `src/test_db/console/_command_name.py`
2. Register in `src/test_db/tdb_console.py`
3. Add tests in `tests/cli/tdb_console/test_tdb_console_command_name.py`

### Adding Database Models

1. Create model in `src/test_db/_model_name.py`
2. Create view in `src/test_db/_views/_model_name.py`
3. Add CLI and console commands for CRUD operations
4. Add comprehensive tests in `tests/test_model_name.py`

## Database Support

The project supports multiple databases:

- **SQLite**: Default, no driver needed
- **PostgreSQL**: Requires `psycopg[binary]`
- **MySQL**: Requires `mysqlclient`

Test across databases by setting `PYTEST_DATABASE_CONNECTION_URI`:

```bash
# Test with PostgreSQL
export PYTEST_DATABASE_CONNECTION_URI="postgresql://user:pass@localhost/testdb"
make test

# Test with MySQL
export PYTEST_DATABASE_CONNECTION_URI="mysql://user:pass@localhost/testdb"
make test
```

## Testing Guidelines

- Aim for >85% code coverage
- Write tests for both success and error paths
- Use descriptive test names following the pattern: `test_feature_scenario`
- Group related tests in test functions
- Use pytest fixtures for common setup (see `tests/conftest.py`)

## Documentation

- Update `README.md` for user-facing changes
- Add/update docstrings for new functions (Google style)
- Document architecture changes in commit messages

## Commit Messages

Use clear, descriptive commit messages that follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary):

```
feat/fix/chore/docs: Brief description (50 chars max)

Optional longer explanation describing:
- What changed and why
- How it affects users
- Any breaking changes
```

Example:
```
feat: Add bulk import for organizations

Implement new bulk import functionality to enable users to load
multiple organizations from CSV files. Includes progress reporting
and transaction rollback on validation errors.
```

## Pull Request Process

1. Ensure all tests pass: `make test`
2. Ensure code quality: `make lint type-check`
3. Update documentation if needed
4. Push to your branch and create a pull request
5. Provide clear description of changes
6. Link any related issues

## Reporting Issues

When reporting bugs, include:

- Python version and OS
- Reproduction steps
- Expected vs actual behavior
- Relevant logs or error messages
- Database type if applicable

## Questions?

- Check existing [GitHub issues](https://github.com/chriskauffman/test-db/issues)
- Review [architecture documentation](./README.md#architecture-overview)
- Examine test cases for usage examples

Thank you for contributing!
