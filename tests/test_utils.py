from tools.utils import Scope


def test_scope_string():
    assert str(Scope.STUDENT) == "olin:student"
