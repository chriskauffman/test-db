import os
import pathlib
# import shutil

# import sqlite3

import test_db as db

from test_db._database_controller import (
    APPLICATION_ID,
    CURRENT_APPLICATION_SCHEMA_VERSION,
    DatabaseController,
)
from test_db._person import Person


def db_schema_is_valid(test_db):
    assert (
        test_db._rawCursor.execute("PRAGMA application_id").fetchone()[0]
        == APPLICATION_ID
    )
    assert test_db._rawCursor.execute("PRAGMA schema_version").fetchone()[0] > 0
    assert (
        test_db._rawCursor.execute("PRAGMA user_version").fetchone()[0]
        == CURRENT_APPLICATION_SCHEMA_VERSION
    )

    assert (
        len(
            test_db._rawCursor.execute(
                f"PRAGMA index_list({db.PersonalBankAccount.sqlmeta.table})"
            ).fetchall()
        )
        == 2
    )
    assert (
        len(
            test_db._rawCursor.execute(
                f"PRAGMA index_list({db.PersonalDebitCard.sqlmeta.table})"
            ).fetchall()
        )
        == 2
    )
    assert (
        len(
            test_db._rawCursor.execute(
                f"PRAGMA index_list({db.Job.sqlmeta.table})"
            ).fetchall()
        )
        == 1
    )
    assert (
        len(
            test_db._rawCursor.execute(
                f"PRAGMA index_list({db.PersonalOAuth2Token.sqlmeta.table})"
            ).fetchall()
        )
        == 2
    )

    assert test_db.validSchema

    return True


def test_init():
    test_db = DatabaseController(db.IN_MEMORY_DB_FILE, create=True)

    assert isinstance(test_db.filePath, pathlib.Path)
    assert test_db.connection
    assert db_schema_is_valid(test_db)


def test_multiple_memory_connections(tmp_path_factory):
    test_db_1 = DatabaseController(db.IN_MEMORY_DB_FILE, create=True)
    test_db_2 = DatabaseController(db.IN_MEMORY_DB_FILE, create=True)

    # Note: two memory db's seem to have one connection
    assert test_db_1.connection == test_db_2.connection

    # __connection__ = test_db_1.connection
    # assert test_db_1.connection == Person(connection=test_db_1.connection)._connection

    # __connection__ = test_db_2.connection
    # assert test_db_2.connection == Person(connection=test_db_2.connection)._connection


def test_multiple_file_connections(tmp_path_factory):
    test_db_1 = DatabaseController(
        tmp_path_factory.mktemp("data") / "test_multiple_connections_1.sqlite",
        create=True,
    )
    test_db_2 = DatabaseController(
        tmp_path_factory.mktemp("data") / "test_multiple_connections_2.sqlite",
        create=True,
    )

    assert test_db_1.connection != test_db_2.connection

    # __connection__ = test_db_1.connection
    assert test_db_1.connection == Person(connection=test_db_1.connection)._connection

    # __connection__ = test_db_2.connection
    assert test_db_2.connection == Person(connection=test_db_2.connection)._connection


# def test_file_0_upgrade(tmp_path_factory):
#     db.databaseEncryptionKey = "a test key"
#     db_file = tmp_path_factory.mktemp("data") / "upgrade_0.sqlite"
#     shutil.copy2("tests/data/test.0.sqlite", db_file)

#     raw_connection = sqlite3.connect(db_file)
#     raw_cursor = raw_connection.cursor()

#     assert raw_cursor.execute("PRAGMA application_id").fetchone()[0] == 0
#     assert raw_cursor.execute("PRAGMA user_version").fetchone()[0] == 0

#     test_db = DatabaseController(db_file, defaultConnection=True)

#     assert db_schema_is_valid(test_db)


# def test_file_3_upgrade(tmp_path_factory):
#     db.databaseEncryptionKey = "a test key"
#     db_file = tmp_path_factory.mktemp("data") / "upgrade_3.sqlite"
#     shutil.copy2("tests/data/test.3.sqlite", db_file)

#     raw_connection = sqlite3.connect(db_file)
#     raw_cursor = raw_connection.cursor()

#     assert raw_cursor.execute("PRAGMA application_id").fetchone()[0] == APPLICATION_ID
#     assert raw_cursor.execute("PRAGMA user_version").fetchone()[0] == 3

#     test_db = DatabaseController(db_file, defaultConnection=True)

#     assert db_schema_is_valid(test_db)


def test_file_version_1(tmp_path_factory):
    db.databaseEncryptionKey = "a test key"
    db_file = tmp_path_factory.mktemp("data") / "test_1.sqlite"
    # shutil.copy2("tests/data/test.9.sqlite", db_file)

    test_db = DatabaseController(db_file, create=True, defaultConnection=True)

    assert db_schema_is_valid(test_db)


def test_open_empty(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "empty.sqlite"
    if os.path.isfile(db_file):
        os.remove(db_file)
    test_db = DatabaseController(db_file, create=True)

    assert db_schema_is_valid(test_db)

    test_users = Person.select(connection=test_db.connection)

    assert not test_users.count()
