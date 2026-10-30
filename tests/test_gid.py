from typeid import TypeID

from test_db._gid import validGID


def test_validGID(temporary_db):
    test_id = TypeID("abc")
    assert validGID(test_id, "abc")
    assert validGID(test_id)
    assert validGID(str(test_id), "abc")
    assert validGID(str(test_id))


def test_invalidGID(temporary_db):
    assert not validGID(TypeID("a"), "b")
    assert not validGID("a_01khke4jvgfjgab8tzxpf8t1sq", "b")  # invalid prefix
    assert not validGID("")  # Invalid typeID string
    assert not validGID("___01khke4jvgfjgab8tzxpf8t1sq")  # Invalid prefix
    assert not validGID("x_invalidGID", "x")  # Invalid suffix
