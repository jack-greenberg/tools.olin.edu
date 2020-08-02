from flask import session, g
from graphene import Mutation, List, ObjectType, String, Int, Field, ID, Enum, Argument
from graphene_sqlalchemy import SQLAlchemyObjectType

from tools.utils import Role as RoleEnum, TrainingStatus as TrainingStatusEnum
from tools.database.models import User as UserModel, UserTraining as UserTrainingModel

Role = Enum.from_enum(RoleEnum)
TrainingStatus = Enum.from_enum(TrainingStatusEnum)
MICROSOFT_GRAPH = "https://graph.microsoft.com/v1.0"

#########
# Schemas
#########
class UserTraining(SQLAlchemyObjectType):
    class Meta:
        model = UserTrainingModel


class User(ObjectType):
    id = ID()
    user_id = String()
    email = String()

    role = Role()

    display_name = String()
    first_name = String()
    last_name = String()
    class_year = Int()

    trainings = List(UserTraining)


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
        role = Role(required=True)

    Output = User

    @staticmethod
    def mutate(self, info, **kwargs):
        id = kwargs.pop("id")
        kwargs["role"] = RoleEnum(kwargs.get("role"))
        user = g.db_session.query(UserModel).get(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        return user


class NewUserTraining(Mutation):
    class Arguments:
        user_id = ID(required=True)
        training_id = ID(required=True)

    Output = User

    def mutate(self, info, **kwargs):
        user_id = kwargs.get("user_id")
        kwargs["status"] = TrainingStatusEnum.STARTED
        user_training = UserTrainingModel(**kwargs)
        user = g.db_session.query(UserModel).filter_by(id=user_id).first()
        user.trainings.append(user_training)
        g.db_session.flush()
        return user


class UpdateTrainingStatus(Mutation):
    class Arguments:
        user_id = ID(required=True)
        training_id = ID(required=True)
        status = Argument(UserTraining.enum_for_field("status"))

    Output = UserTraining

    def mutate(self, info, **kwargs):
        new_status = TrainingStatusEnum(kwargs.pop("status", None))
        user_training = (
            g.db_session.query(UserTrainingModel).filter_by(**kwargs).first()
        )
        setattr(user_training, "status", new_status)
        return user_training


class UserMutation(ObjectType):
    update_user_role = UpdateUserRole.Field()
    add_user_training = NewUserTraining.Field()
    update_training_status = UpdateTrainingStatus.Field()
