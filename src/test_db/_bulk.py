from collections.abc import Callable
from typing import Any

_UNIQUE_FIELDS = {
    "person": (
        ("firstName", "lastName"),
        ("email",),
        ("phoneNumber",),
        ("socialSecurityNumber",),
    ),
    "organization": (("name",), ("employerIdentificationNumber",)),
    "person_address": (("street", "locality", "region", "postalCode"),),
    "organization_address": (("street", "locality", "region", "postalCode"),),
    "person_bank_account": (("routingNumber", "accountNumber"),),
    "organization_bank_account": (("routingNumber", "accountNumber"),),
    "person_debit_card": (("cardNumber",),),
}


def bulk_unique(
    connection: Any,
    model: Any,
    fields: tuple[str, ...],
    generator: Callable[[], Any],
) -> Any | None:
    """Generate a value not already present in a bulk operation.

    Existing values are loaded into compact field-value sets once per model.
    Returns None when the connection is not in bulk mode.
    """
    if connection is None:
        return None
    options = connection.tdbGlobalDatabaseOptions
    if not options.bulkAdd:
        return None

    key = (model, fields)
    if model not in options.bulkUniqueModels:
        unique_fields: set[tuple[str, ...]] = {
            tuple(field_set)
            for field_set in _UNIQUE_FIELDS.get(model.sqlmeta.table, ())
        }
        unique_fields.add(fields)
        rows = model.select(connection=connection)
        values = {field_set: set() for field_set in unique_fields}
        for row in rows:
            for field_set, seen in values.items():
                seen.add(tuple(getattr(row, field) for field in field_set))
        options.bulkUniqueValues.update(
            {(model, field_set): seen for field_set, seen in values.items()}
        )
        options.bulkUniqueModels.add(model)

    seen = options.bulkUniqueValues[key]

    while True:
        value = generator()
        candidate = value if isinstance(value, tuple) else (value,)
        if candidate not in seen:
            seen.add(candidate)
            return value
