from graphene import Mutation, ObjectType, Field, List, ID, Int
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
    training = Field(Training, id=Int(required=True))
    trainings = List(Training)

    def resolve_training(self, info, id=None, **kwargs):
        pass

    def resolve_trainings(self, info, **kwargs):
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
