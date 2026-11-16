from collections.abc import Callable
from typing import Any


def bulk_unique(
    connection: Any,
    model: Any,
    fields: tuple[str, ...],
    generator: Callable[[], Any],
) -> Any | None:
    """Generate a value not already present in a bulk operation.

    Existing values are loaded into a field-value set once per model and field
    combination. Returns None when the connection is not in bulk mode.
    """
    if connection is None:
        return None
    options = connection.tdbGlobalDatabaseOptions
    if not options.bulkAdd:
        return None

    key = (model, fields)
    seen = options.bulkUniqueValues.get(key)
    if seen is None:
        rows = model.select(connection=connection)
        seen = {tuple(getattr(row, field) for field in fields) for row in rows}
        options.bulkUniqueValues[key] = seen

    while True:
        value = generator()
        candidate = value if isinstance(value, tuple) else (value,)
        if candidate not in seen:
            seen.add(candidate)
            return value
