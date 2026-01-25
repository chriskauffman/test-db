# dex-tools Makefile

.PHONY: build
build: lint type-check test src/test_db/_schemas/v1.sql
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

.PHONY: type-check
type-check:
	uv run mypy src/*

.PHONY: test
test:
	uv run pytest

.PHONY: command-test
command-test:
	uv run tdb --version

src/test_db/_schemas/v1.sql: tests/data/test_schema_v1.sqlite
	sqlite3 --readonly tests/data/test_schema_v1.sqlite .schema > $@

tests/data/test_schema_v1.sqlite: src/test_db/*.py
	rm -f tests/data/test_schema_v1.sqlite
	uv run tdb --no-upgrade --db-connection-uri "sqlite:tests/data/test_schema_v1.sqlite" version

.PHONY: init
init: log tmp
	brew install --quiet prettier uv yamllint
	uv sync --all-groups

log tmp:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .ruff_cache
	-rm -rf .venv
	-rm -rf dist
	-rm -rf log
