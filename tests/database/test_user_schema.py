from tools.database.models import User
from tools.utils import Role


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
