from flask import current_app
from graphene import Mutation, List, ObjectType, String, Field, ID, Enum

from tools.utils import Role as RoleEnum

Role = Enum.from_enum(RoleEnum)

#########
# Schemas
#########
class User(ObjectType):
    id = ID()
    mail = String()

    displayName = String()
    givenName = String()
    surname = String()
    role = Role()

    def resolve_role(self, info):
        pass


#########
# Queries
#########
class UserQuery(ObjectType):
    """
    Example:
    query {
        user (
            id: 0
        ) {
            name
            first_name
            email
            trainings {
                tool_level {
                    tool {
                        name
                        category
                    }
                }
            }
        }
    }
    """

    user = Field(User, id=ID(required=True))
    users = List(User)

    def resolve_user(self, info, id=None):
        response = current_app.auth.get_current_user()
        return response


###########
# Mutations
###########
class AddUser(Mutation):
    class Arguments:
        name = String(required=True)
        role = Role()

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        pass


# class UpdateUserRole(Mutation):
#     class Arguments:
#         id = Int(required=True)
#         role = Role()
#
#     Output = User
#
#     @staticmethod
#     def mutate(self, info, **kwargs):
#         id = kwargs.pop("id")
#         kwargs["role"] = Role(kwargs["role"])
#         user = g.db_session.query(UserModel).get(id)
#         for key, value in kwargs.items():
#             setattr(user, key, value)
#         return user


class UserMutation(ObjectType):
    add_user = AddUser.Field()
