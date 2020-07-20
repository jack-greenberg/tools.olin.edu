from tools.utils import Scope
from tools.database.user import User


def create_mock_user(user_id, db_session):
    user = User(
        id=user_id,
        name="alovelace",
        email="alovelace@example.com",
        scope=Scope.ADMIN,
        first_name="Ada",
        last_name="Lovelace",
        class_year=2023,
    )

    db_session.add(user)
    # db_session.commit()

    return user
