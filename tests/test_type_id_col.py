import pytest

from typeid import TypeID

from sqlobject import connectionForURI, SQLObject
from formencode import validators  # type: ignore

from test_db._type_id_col import TypeIDCol


class ObjectWithTypeId(SQLObject):
    tid: TypeIDCol = TypeIDCol(alternateID=True, default=TypeID)
    nullableTid: TypeIDCol = TypeIDCol(default=None)


@pytest.fixture(scope="session")
def type_id_db(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "type_id_db.sqlite"
    connection = connectionForURI(f"sqlite:{db_file}")
    ObjectWithTypeId.createTable(connection=connection)
    return connection


def test_set_various_values(type_id_db):
    test_object = ObjectWithTypeId(
        tid=TypeID("tdb"),
        connection=type_id_db,
    )

    assert isinstance(test_object.tid, TypeID)
    assert ObjectWithTypeId.byTid(test_object.tid, connection=type_id_db) is test_object
    assert (
        ObjectWithTypeId.byTid(str(test_object.tid), connection=type_id_db)
        is test_object
    )

    assert ObjectWithTypeId(connection=type_id_db)
    assert ObjectWithTypeId(nullableTid=None, connection=type_id_db)

    with pytest.raises(validators.Invalid):
        ObjectWithTypeId(tid="___01khke4jvgfjgab8tzxpf8t1sq", connection=type_id_db)
