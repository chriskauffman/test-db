from test_db._employer import Employer


def test_employer(temporary_db):
    test_employer = Employer(
        name="test_employer",
        connection=temporary_db.connection,
    )

    assert isinstance(test_employer, Employer)
