from test_db._gid_sqlobject import GID_SQLObject


def test_gid_sqlobject(temporary_db):
    GID_SQLObject.createTable(connection=temporary_db.connection)
    test_full_sqlobject = GID_SQLObject(
        connection=temporary_db.connection,
    )

    assert isinstance(test_full_sqlobject, GID_SQLObject)
