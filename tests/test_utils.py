from tools.utils import Role


def test_scope_string():
    assert str(Role.STUDENT) == "olin:student"
