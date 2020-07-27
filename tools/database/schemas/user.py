from flask import session, g
from graphene import Mutation, List, ObjectType, String, Field, ID, Enum

from tools.utils import Role as RoleEnum
from tools.database.models import User as UserModel

Role = Enum.from_enum(RoleEnum)
MICROSOFT_GRAPH = "https://graph.microsoft.com/v1.0"

#########
# Schemas
#########
class User(ObjectType):
    id = ID()
    user_id = String()
    email = String()

    first_name = String()
    last_name = String()
    display_name = String()
    role = Role()


#########
# Queries
#########
class UserQuery(ObjectType):
    """
    Example:
    query {
        user (
            id: 1
        ) {
            id
            givenName
            role
        }
    }
    """

    me = Field(User)
    user = Field(User, id=ID(required=True))
    users = List(User)

    def resolve_me(self, info):
        my_id = session.get("user").get("oid")
        me = g.db_session.query(UserModel).filter_by(user_id=my_id).first()
        return me

    def resolve_user(self, info, id=None):  # id or user_id?
        user = g.db_session.query(UserModel).filter_by(id=id).first()
        return user

    def resolve_users(self, info):
        users = g.db_session.query(UserModel).all()
        return users


###########
# Mutations
###########
class UpdateUserRole(Mutation):
    class Arguments:
        id = ID(required=True)
        role = Role()

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        id = kwargs.pop("id")
        kwargs["role"] = RoleEnum(kwargs["role"])
        user = g.db_session.query(UserModel).get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        return user


class UserMutation(ObjectType):
    update_user_role = UpdateUserRole.Field()
