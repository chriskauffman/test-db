import pytest

from test_db._entity import Entity


@pytest.fixture(scope="session", autouse=True)
def set_autoCreate_dependents():
    Entity._autoCreateDependents = True


def test_init(temporary_db):
    test_entity = Entity(connection=temporary_db.connection)
    assert test_entity
