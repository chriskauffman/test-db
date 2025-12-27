# test-db

Python Test Database That Automatically Generates Test Data

## Database Connections

test-db should support any valid [SQLObject connection](https://sqlobject.readthedocs.io/en/stable/SQLObject.html#declaring-a-connection).

Pytest supports the connection environment variable `PYTEST_DATABASE_CONNECTION_URI`.
If this is set with a valid SQLObject connection URI such as `export PYTEST_DATABASE_CONNECTION_URI=postgres://test_db:BADPASSWORD@nas02/test_db`
it will be used to execute tests when `uv run pytest` or `make` is executed. If it
is unset, tests will run against a sqlite file.

Note: You must install database drivers to support the conection specified, such as `uv add "psycopg[binary]"
