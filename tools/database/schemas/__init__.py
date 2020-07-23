from graphene import Schema as BaseSchema

from .user import UserQuery, UserMutation

from .tool import ToolQuery, ToolMutation

__all__ = ["AppSchema"]


class BaseQuery(UserQuery, ToolQuery):
    pass


class BaseMutation(UserMutation, ToolMutation):
    pass


AppSchema = BaseSchema(query=BaseQuery, mutation=BaseMutation)
