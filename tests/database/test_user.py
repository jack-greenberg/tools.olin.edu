from tests.fixtures.user import create_mock_user
from tools.database.user import User


def test_init_user(db_session):
    create_mock_user(0, db_session)
    assert db_session.query(User).all()
