from test_db._full_sqlobject import FullSQLObject


def test_full_sqlobject(temporary_db):
    FullSQLObject.createTable(connection=temporary_db.connection)
    test_full_sqlobject = FullSQLObject(
        connection=temporary_db.connection,
    )

    assert isinstance(test_full_sqlobject, FullSQLObject)
