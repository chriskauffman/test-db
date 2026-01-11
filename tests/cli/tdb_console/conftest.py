import os
import pytest


@pytest.fixture(scope="module", autouse=True)
def set_env(temporary_db):
    # setting DB connection to avoid defaulting to a real DB in tests
    os.environ["DB_CONNECTION_URI"] = temporary_db.connectionURI
