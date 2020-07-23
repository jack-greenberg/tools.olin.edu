#  import graphene
#  from graphene import Enum, Field, Int, Mutation, ObjectType, String
#  from .models import User as UserModel
#  from tools.utils import Role
#  from tools.database import db_context
#
#  from . import RoleEnum
#  from .user import User
#  from .tool import Tool, ToolLevel
#
#  """
#  Schemas
#  """
#
#
#  class Training(ObjectType):
#  id = Int()
#  user = User()
#  tool_level = ToolLevel()
#
#  @db_context
#  def resolve_tool(self, info, tool_id):
#  pass
#
#
#  """
#  Queries
#  """
#
#
#  class TrainingQuery(ObjectType):
#  pass
