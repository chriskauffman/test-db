# test-db

Python Test Database That Automatically Generates Test Data

## Database Connections

test-db should support any valid [SQLObject connection](https://sqlobject.readthedocs.io/en/stable/SQLObject.html#declaring-a-connection).

Pytest supports the connection environment variable `PYTEST_DATABASE_CONNECTION_URI`.
If this is set with a valid SQLObject connection URI such as `export PYTEST_DATABASE_CONNECTION_URI=postgres://REPLACE_WITH_USER_ID:REPLACE_WITH_PASSWORD@REPLACE_WITH_SERVER/REPLACE_WITH_DATABASE` or `export PYTEST_DATABASE_CONNECTION_URI=mysql://REPLACE_WITH_USER_ID:REPLACE_WITH_PASSWORD@REPLACE_WITH_SERVER/REPLACE_WITH_DATABASE`
it will be used to execute tests when `uv run pytest` or `make` is executed. If it
is unset, tests will run against a sqlite file.

Note: You must install database drivers to support the conection specified, such as `uv add "psycopg[binary]"

### Installation of Utilities

For general use with sqlite:
`uv tool install --python 3.14 git+ssh://git@github.com/chriskauffman/test-db.git`

For use with additional databases:
`uv tool install --python 3.14 --with "psycopg[binary]" --with "mysqlclient" git+ssh://git@github.com/chriskauffman/test-db.git`

Once installed, upgrades may be handled with: `uv tool upgrade test-db`

### Execution directly without install

`uvx --from git+ssh://git@github.com/chriskauffman/test-db.git --python 3.14 tdb job list`

`uvx --from git+ssh://git@github.com/chriskauffman/test-db.git --with "psycopg[binary]" --python 3.14 tdb -d postgres://REPLACE_WITH_USER_ID:REPLACE_WITH_PASSWORD@REPLACE_WITH_SERVER/REPLACE_WITH_DATABASE job list`

### Resetting Databases

`mariadb -u root -h REPLACE_WITH_SERVER -p < reset_mysql.sql`
`psql -h REPLACE_WITH_SERVER -U postgres -f reset_postgresql.sql`
