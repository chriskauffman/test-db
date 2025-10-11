from test_db._address import Address


def test_address(temporary_db):
    test_address = Address(connection=temporary_db.connection)

    assert isinstance(test_address, Address)
