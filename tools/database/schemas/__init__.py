from graphene import Schema as BaseSchema

from .user import UserQuery, UserMutation
from .tool import ToolQuery, ToolMutation
from .training import TrainingQuery, TrainingMutation

__all__ = ["AppSchema"]


class BaseQuery(UserQuery, ToolQuery, TrainingQuery):
    pass


class BaseMutation(UserMutation, ToolMutation, TrainingMutation):
    pass


AppSchema = BaseSchema(query=BaseQuery, mutation=BaseMutation)
