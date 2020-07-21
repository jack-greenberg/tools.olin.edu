from graphene import Schema as BaseSchema

from .user import UserQuery, UserMutation

# from .tool import ToolQuery, ToolMutation

__all__ = ["AppSchema"]

"""
Enums
"""


"""
Base Objects
"""


class BaseQuery(UserQuery):
    # node = relay.Node.Field()
    pass


class BaseMutation(UserMutation):
    pass


AppSchema = BaseSchema(query=BaseQuery, mutation=BaseMutation)
