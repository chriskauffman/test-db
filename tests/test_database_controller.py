import os
import shutil

import test_db

from test_db._database_controller import DatabaseController
from test_db._person import Person


def db_schema_is_valid(database_contoller):
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA application_id").fetchone()[0]
    #     == APPLICATION_ID
    # )
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA schema_version").fetchone()[0] > 0
    # )
    # assert (
    #     database_contoller._rawCursor.execute("PRAGMA user_version").fetchone()[0]
    #     == CURRENT_APPLICATION_SCHEMA_VERSION
    # )

    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.BankAccount.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )
    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.DebitCard.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )
    # assert (
    #     len(
    #         database_contoller._rawCursor.execute(
    #             f"PRAGMA index_list({test_db.Job.sqlmeta.table})"
    #         ).fetchall()
    #     )
    #     == 2
    # )

    assert database_contoller.validSchema

    return True


def test_init():
    db = DatabaseController(test_db.IN_MEMORY_DB_FILE)

    # assert isinstance(db.filePath, pathlib.Path)
    assert db.connection
    assert db_schema_is_valid(db)


def test_multiple_memory_connections(tmp_path_factory):
    db_1 = DatabaseController(test_db.IN_MEMORY_DB_FILE)
    db_2 = DatabaseController(test_db.IN_MEMORY_DB_FILE)

    # Note: two memory db's seem to have one connection
    assert db_1.connection == db_2.connection

    # __connection__ = db_1.connection
    # assert db_1.connection == Person(connection=db_1.connection)._connection

    # __connection__ = db_2.connection
    # assert db_2.connection == Person(connection=db_2.connection)._connection


def test_multiple_file_connections(tmp_path_factory):
    db_1_file = tmp_path_factory.mktemp("data") / "test_multiple_connections_1.sqlite"
    db_1 = DatabaseController(f"sqlite://{db_1_file}")
    db_2_file = tmp_path_factory.mktemp("data") / "test_multiple_connections_2.sqlite"
    db_2 = DatabaseController(f"sqlite://{db_2_file}")

    assert db_1.connection != db_2.connection

    # __connection__ = db_1.connection
    assert db_1.connection == Person(connection=db_1.connection)._connection

    # __connection__ = db_2.connection
    assert db_2.connection == Person(connection=db_2.connection)._connection


# def test_schema_X_upgrade(tmp_path_factory):
#     test_db.databaseEncryptionKey = "a test key"
#     db_file = tmp_path_factory.mktemp("data") / "upgrade_0.sqlite"
#     shutil.copy2("tests/data/test.0.sqlite", db_file)

#     raw_connection = sqlite3.connect(db_file)
#     raw_cursor = raw_connection.cursor()

#     assert raw_cursor.execute("PRAGMA application_id").fetchone()[0] == 0
#     assert raw_cursor.execute("PRAGMA user_version").fetchone()[0] == 0

#     test_db = DatabaseController(db_file, defaultConnection=True)

#     assert db_schema_is_valid(test_db)


def test_file_version_1(tmp_path_factory):
    test_db.databaseEncryptionKey = "a test key"
    db_file = tmp_path_factory.mktemp("data") / "test_file_version_1.sqlite"
    # shutil.copy2("tests/data/test.9.sqlite", db_file)

    db = DatabaseController(f"sqlite://{db_file}")

    assert db_schema_is_valid(db)


def test_open_empty(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_open_empty.sqlite"
    if os.path.isfile(db_file):
        os.remove(db_file)
    test_db = DatabaseController(f"sqlite://{db_file}")

    assert test_db.validSchema

    test_users = Person.select(connection=test_db.connection)

    assert not test_users.count()


def test_open_empty_existing_file(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_open_empty_existing_file.sqlite"
    shutil.copy2("tests/data/test_empty.sqlite", db_file)

    test_db = DatabaseController(f"sqlite://{db_file}")

    assert db_schema_is_valid(test_db)

    test_users = Person.select(connection=test_db.connection)

    assert not test_users.count()
