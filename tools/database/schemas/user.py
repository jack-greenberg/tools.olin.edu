from flask import g
from graphene import Int, Mutation, List, ObjectType, String, Argument, Field
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel
from tools.utils import Role

#########
# Schemas
#########


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


#########
# Queries
#########
class UserQuery(ObjectType):
    user = Field(User, id=Int(required=True))
    users = List(User)

    def resolve_user(self, info, id=None, **kwargs):
        user_query = g.db_session.query(UserModel).filter_by(id=id)
        return user_query.first()

    def resolve_users(self, info):
        return g.db_session.query(UserModel).all()


###########
# Mutations
###########
class AddUser(Mutation):
    class Arguments:
        name = String(required=True)
        role = Argument(User.enum_for_field("role"))

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        kwargs["role"] = Role(kwargs["role"])
        new_user = UserModel(**kwargs)
        g.db_session.add(new_user)
        g.db_session.flush()
        return new_user


class UpdateUserRole(Mutation):
    class Arguments:
        id = Int(required=True)
        role = Argument(User.enum_for_field("role"))

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        id = kwargs.pop("id")
        kwargs["role"] = Role(kwargs["role"])
        user = g.db_session.query(UserModel).get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        return user


class UserMutation(ObjectType):
    add_user = AddUser.Field()
    update_user = UpdateUserRole.Field()
