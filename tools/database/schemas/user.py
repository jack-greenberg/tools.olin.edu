import requests

from flask import current_app, session, g
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
    mail = String()

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
            id: "asdf-1234567890-asdfhjjkl"
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
        user_id = session.get("user").get("oid")
        user = g.db_session.query(UserModel).filter_by(user_id=user_id).first()
        return user

    def resolve_user(self, info, id=None):
        selection = ["id", "displayName", "mail", "givenName", "surname"]
        response = requests.get(
            MICROSOFT_GRAPH + "/user/{id}".format(id=id),
            params={"$select": ",".join(selection)},
            headers=current_app.auth.get_auth_headers(),
        ).json()
        return response

    def resolve_users(self, info):
        pass


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
        pass
        # id = kwargs.pop("id")
        # kwargs["role"] = Role(kwargs["role"])
        # user = g.db_session.query(UserModel).get(id)
        # for key, value in kwargs.items():
        #     setattr(user, key, value)
        # return user


class UserMutation(ObjectType):
    update_user_role = UpdateUserRole.Field()
    # add_user = AddUser.Field()
