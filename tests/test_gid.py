from typeid import TypeID

from test_db._gid import validGID


def test_validGID(temporary_db):
    test_id = TypeID("abc")
    assert validGID(test_id, "abc")


def test_invalidGID(temporary_db):
    assert not validGID("a_01khke4jvgfjgab8tzxpf8t1sq", "b")  # invalid prefix
    assert not validGID(123)  # not str
    assert not validGID("")  # Invalid typeID string
    assert not validGID("___01khke4jvgfjgab8tzxpf8t1sq")  # Invalid prefix
    assert not validGID("x_invalidGID", "x")  # Invalid suffix
