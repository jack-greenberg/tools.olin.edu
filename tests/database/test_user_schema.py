from tools.database.models import User
from tools.utils import Role
from tests.conftest import mock_user, mock_tool, mock_training


def test_session(db_session):
    user = User(
        user_id="12345-67890-asdfhjkl",
        first_name="Test",
        last_name="Person",
        email="test@olin.edu",
        role=Role.STUDENT,
    )

    db_session.add(user)
    db_session.flush()
    db_session.commit()

    result = db_session.query(User).filter_by(user_id="12345-67890-asdfhjkl").first()

    assert user.user_id == result.user_id


def test_mocks(db_session):
    u = mock_user(1, db_session)
    t = mock_tool(1, db_session)
    tr = mock_training(1, db_session=db_session, tools=[t])
    assert u in db_session
    assert tr.tools == [t]
    assert u.id == 1
