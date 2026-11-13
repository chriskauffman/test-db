# test-db Makefile

.PHONY: build
build: lint type-check test test-migration-sqlite security-audit src/test_db/_schemas/v2.sql
	uv build

.PHONY:
format:
	uv run ruff format
	prettier -w README.md .github/

.PHONY: lint
lint:
	uv run ruff format --check
	uv run ruff check
	uv run pydoclint --style google src/
	uv run pydoclint --style google tests/
	yamllint .github/

.PHONY: security-audit
security-audit:
	uv audit

.PHONY: type-check
type-check:
	uv run ty check

.PHONY: test
test:
	uv run pytest

.PHONY: test-mysql
test-mysql:
	PYTEST_DATABASE_CONNECTION_URI="mysql://test_db@nas02/test_db" uv run pytest

.PHONY: test-postgresql
test-postgresql:
	PYTEST_DATABASE_CONNECTION_URI="postgresql://test_db@nas02/test_db" uv run pytest

.PHONY: test-migration-mysql
test-migration-mysql:
	PYTEST_MIGRATION_DATABASE_CONNECTION_URI="mysql://test_db@nas02/test_db" PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1 uv run pytest -m migration tests/migrations

.PHONY: test-migration-postgresql
test-migration-postgresql:
	PYTEST_MIGRATION_DATABASE_CONNECTION_URI="postgresql://test_db@nas02/test_db" PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1 uv run pytest -m migration tests/migrations

.PHONY: test-migration-sqlite
test-migration-sqlite:
	cp tests/data/test_schema_v2.sqlite tmp/v1_migration_test.sqlite
	PYTEST_MIGRATION_DATABASE_CONNECTION_URI="sqlite:tmp/v1_migration_test.sqlite" PYTEST_ALLOW_DESTRUCTIVE_MIGRATION_TESTS=1 uv run pytest -m migration tests/migrations

.PHONY: coverage
coverage:
	uv run coverage run -m pytest && uv run coverage report --show-missing

.PHONY: command-test
command-test:
	uv run tdb version
	uv run tdb-console version quit

src/test_db/_schemas/v2.sql: src/test_db/*.py | tmp
	rm -f tmp/test_schema_v2.sqlite
	uv run tdb --db-connection-uri "sqlite:tmp/test_schema_v2.sqlite" person list >/dev/null
	sqlite3 --readonly tmp/test_schema_v2.sqlite .schema > $@

tests/data/test_schema_v2.sqlite: src/test_db/_schemas/v2.sql
	rm -f tests/data/test_schema_v2.sqlite
	uv run tdb --db-connection-uri "sqlite:tests/data/test_schema_v2.sqlite" person list >/dev/null

.PHONY: init
init: backup log tmp
	brew install --quiet mariadb postgresql@17 prettier uv yamllint
	uv sync --all-groups

backup log tmp:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -rf .pytest_cache
	-rm -rf .ruff_cache
	-rm -rf .venv
	-rm -rf dist
	-rm -rf log
