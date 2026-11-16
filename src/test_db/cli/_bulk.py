from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


@contextmanager
def bulk_transaction(connection: Any) -> Generator[Any, None, None]:
    """Run one bulk operation with in-memory Faker uniqueness tracking."""
    transaction = connection.transaction()
    options = connection.tdbGlobalDatabaseOptions
    options.bulkAdd = True
    options.bulkUniqueValues.clear()
    try:
        yield transaction
        transaction.commit(close=True)
    except Exception:
        transaction.rollback()
        raise
    finally:
        options.bulkAdd = False
        options.bulkUniqueValues.clear()
