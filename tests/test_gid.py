from typeid import TypeID

from test_db._gid import validGID


def test_validGID(temporary_db):
    test_id = TypeID("abc")
    assert validGID(test_id, "abc")
