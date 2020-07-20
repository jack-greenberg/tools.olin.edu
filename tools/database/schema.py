import graphene
from graphene import Enum, Field, Int, Mutation, ObjectType, String
from .models import User as UserModel
from tools.utils import Role
from tools.database import db_session


RoleEnum = Enum.from_enum(Role)


class User(ObjectType):
    id = Int()
    name = String()
    email = String()
    role = RoleEnum()
    first_name = String()
    last_name = String()
    class_year = Int()


class UserQuery(ObjectType):
    user = Field(User, id=Int(required=True))

    def resolve_user(self, info, id):
        user = db_session.query(UserModel).get(id)
        return user


class AddUser(Mutation):
    class Arguments:
        name = String(required=True)
        role = RoleEnum()

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        kwargs["role"] = Role(kwargs["role"])
        new_user = UserModel(**kwargs)
        db_session.add(new_user)
        db_session.commit()

        return new_user


class UpdateUserRole(Mutation):
    class Arguments:
        id = Int(required=True)
        role = RoleEnum()

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        id = kwargs.pop("id")
        kwargs["role"] = Role(kwargs["role"])
        user = db_session.query(UserModel).get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)

        db_session.commit()
        return user


class UserMutation(ObjectType):
    add_user = AddUser.Field()
    update_user = UpdateUserRole.Field()


class Query(UserQuery):
    pass


class Mutation(UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=UserMutation)
