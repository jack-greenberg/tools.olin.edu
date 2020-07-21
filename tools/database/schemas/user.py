from graphene import Field, Int, Mutation, List, ObjectType, String
from .models import User as UserModel
from tools.utils import Role
from tools.database import db_context
from . import RoleEnum
from .tool import Tool

"""
Schemas
"""


class User(ObjectType):
    id = Int()
    name = String()
    email = String()
    role = RoleEnum()
    first_name = String()
    last_name = String()
    class_year = Int()

    tools = List(Tool)


"""
Queries
"""


class UserQuery(ObjectType):
    user = Field(User, id=Int(required=True))

    @db_context
    def resolve_user(self, info, id, db_session=None):
        user = db_session.query(UserModel).get(id)
        return user


"""
Mutations
"""


class AddUser(Mutation):
    class Arguments:
        name = String(required=True)
        role = RoleEnum()

    Output = User

    @staticmethod
    @db_context
    def mutate(self, info, db_session=None, **kwargs):
        kwargs["role"] = Role(kwargs["role"])
        new_user = UserModel(**kwargs)
        db_session.add(new_user)
        return new_user


class UpdateUserRole(Mutation):
    class Arguments:
        id = Int(required=True)
        role = RoleEnum()

    Output = User

    @staticmethod
    @db_context
    def mutate(self, info, db_session=None, **kwargs):
        id = kwargs.pop("id")
        kwargs["role"] = Role(kwargs["role"])
        user = db_session.query(UserModel).get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        return user


class UserMutation(ObjectType):
    add_user = AddUser.Field()
    update_user = UpdateUserRole.Field()
