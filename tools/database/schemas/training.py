from flask import g
from graphene import Mutation, ObjectType, Field, List, Int, String
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Training as TrainingModel, Tool as ToolModel

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
        tool_id = Int()
        tool_ids = List(Int)

        name = String()
        prerequisite_id = Int(required=False)

    Output = Training

    @staticmethod
    def mutate(self, info, **kwargs):
        prereq_id = kwargs.pop("prerequisite_id", None)

        tool_ids = kwargs.pop("tool_ids", None) or [kwargs.pop("tool_id", None)]
        tools = g.db_session.query(ToolModel).filter(ToolModel.id.in_(tool_ids)).all()

        training = TrainingModel(**kwargs)
        training.tools = tools

        if prereq_id:
            prereq = g.db_session.query(TrainingModel).filter_by(id=prereq_id).first()
            training.prerequisite = prereq

        return training


class TrainingMutation(ObjectType):
    add_training = AddTraining.Field()
