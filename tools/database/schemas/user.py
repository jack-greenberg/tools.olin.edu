from graphene import Int, Mutation, List, ObjectType, String, Argument
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel
from tools.utils import Role
from tools.database import Session

# RoleEnum = Enum.from_enum(Role)

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
    users = List(User)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()


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
        db_session = Session()
        kwargs["role"] = Role(kwargs["role"])
        new_user = UserModel(**kwargs)
        db_session.add(new_user)

        return new_user


class UpdateUserRole(Mutation):
    class Arguments:
        id = Int(required=True)
        role = Argument(User.enum_for_field("role"))

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        db_session = Session()
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
