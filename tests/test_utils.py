from tools.utils import Role


def test_scopes():
    assert str(Role.STUDENT) == "olin:student"
    assert Role.NINJA.full() == (Role.BASE, Role.STUDENT, Role.NINJA)
    assert Role.from_str("olin:admin") == Role.ADMIN
