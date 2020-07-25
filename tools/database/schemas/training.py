from graphene import Mutation, ObjectType, List, ID
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Training as TrainingModel

"""
Schemas
"""


class Training(SQLAlchemyObjectType):
    class Meta:
        model = TrainingModel


"""
Queries
"""


class TrainingQuery(ObjectType):
    trainings_for_user = List(Training)

    def resolve_trainings_for_user(self, info, **kwargs):
        pass


"""
Mutations
"""


class AddTraining(Mutation):
    class Arguments:
        user_id = ID(required=True)
        tool_level_id = ID(required=True)

    Output = Training

    @staticmethod
    def mutate(self, info, **kwargs):
        #  user_id = kwargs.pop("user_id")
        #  tool_id = kwargs.pop("tool_id")
        pass


class TrainingMutation(ObjectType):
    add_training = AddTraining.Field()
