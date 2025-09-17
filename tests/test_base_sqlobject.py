from test_db._base_sqlobject import BaseSQLObject


def test_base_sqlobject(temporary_db):
    BaseSQLObject.createTable(connection=temporary_db.connection)
    test_base_sqlobject = BaseSQLObject(
        connection=temporary_db.connection,
    )

    assert isinstance(test_base_sqlobject, BaseSQLObject)
