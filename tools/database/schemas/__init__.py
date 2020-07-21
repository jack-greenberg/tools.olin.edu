from graphene import Schema as BaseSchema, Enum

from tools.utils import Role
from .user import UserQuery, UserMutation

"""
Enums
"""
RoleEnum = Enum.from_enum(Role)


"""
Base Objects
"""


class BaseQuery(UserQuery):
    pass


class BaseMutation(UserMutation):
    pass


AppSchema = BaseSchema(query=BaseQuery, mutation=BaseMutation)
