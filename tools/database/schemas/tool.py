from graphene import Field, Int, Mutation, ObjectType, String, List

from ..models import Tool as ToolModel, ToolCategory as ToolCategoryModel

# from tools.database import db_context

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

    def resolve_category(self, info, db_session=None, **kwargs):
        pass

    def resolve_levels(self, info, db_session=None, **kwargs):
        pass


"""
Queries
"""


class ToolQuery(ObjectType):
    tool = Field(Tool, id=Int(required=True))
    tools_by_category = Field(Tool, category=String(required=True))
    # categories = Field(ToolCategory, name=String(required=True))

    @staticmethod
    def resolve_tool(self, info, id, db_session=None, **kwargs):
        tool = db_session.query(ToolModel).get(id)
        print(tool)
        return tool

    @staticmethod
    def resolve_tools_by_category(self, info, category, db_session=None, **kwargs):
        tools = (
            ToolModel.query.filter.join(ToolCategoryModel, aliased=True)
            .filter_by(name=category)
            .all()
        )

        return tools


"""
Mutations
"""


class AddTool(Mutation):
    class Arguments:
        name = String(required=True)

    Output = Tool

    @staticmethod
    def mutate(self, info, db_session=None, **kwargs):
        new_tool = ToolModel(**kwargs)
        db_session.add(new_tool)
        print(new_tool)
        return new_tool


class ToolMutation(ObjectType):
    add_tool = AddTool.Field()
