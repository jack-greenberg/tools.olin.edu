from graphene import Field, Int, Mutation, ObjectType, String, List

from .models import Tool as ToolModel
from tools.database import db_context

"""
Schemas
"""


class ToolCategory(ObjectType):
    id = Int()
    name = String()


class ToolLevel(ObjectType):
    id = Int()
    name = String()
    prerequisite = Field(lambda: ToolLevel)


class Tool(ObjectType):
    id = Int()
    name = String()
    category = ToolCategory()
    levels = List(ToolLevel)


"""
Queries
"""


class ToolQuery(ObjectType):
    tool = Field(Tool, id=Int(required=True))
    categories = Field(ToolCategory, name=String(required=True))

    @db_context
    def resolve_tool(self, info, id, db_session=None, **kwargs):
        tool = db_session.query(ToolModel).get(id)
        return tool

    @db_context
    def resolve_categories(self, info, name):
        pass


class ToolCategoryQuery(ObjectType):
    pass


"""
Mutations
"""


class AddTool(Mutation):
    class Arguments:
        name = String(required=True)

    Output = Tool

    @staticmethod
    @db_context
    def mutate(self, info, db_session=None, **kwargs):
        new_tool = ToolModel(**kwargs)
        db_session.add(new_tool)
        return new_tool


class ToolMutation(ObjectType):
    add_tool = AddTool.Field()
