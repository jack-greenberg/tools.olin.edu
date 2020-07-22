from graphene import Field, Int, Mutation, ObjectType, String, List
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Tool as ToolModel, ToolCategory as ToolCategoryModel
from tools.database import Session

"""
Schemas
"""


class Tool(SQLAlchemyObjectType):
    class Meta:
        model = ToolModel


class ToolCategory(SQLAlchemyObjectType):
    class Meta:
        model = ToolCategoryModel


"""
Queries
"""


class ToolQuery(ObjectType):
    tool = Field(Tool, id=Int(required=True))
    tools = List(Tool)
    tools_by_category = List(Tool, category=String(required=True))

    @staticmethod
    def resolve_tool(self, info, id):
        query = Tool.get_query(info).filter_by(id=id)
        return query.first()

    @staticmethod
    def resolve_tools(self, info):
        query = Tool.get_query(info)
        return query.all()

    @staticmethod
    def resolve_tools_by_category(self, info, category):
        query = Tool.get_query(info).filter(ToolModel.category.has(name=category))
        return query.all()


"""
Mutations
"""


class AddTool(Mutation):
    class Arguments:
        name = String(required=True)
        category = String()

    Output = Tool

    @staticmethod
    def mutate(self, info, **kwargs):
        db_session = Session()

        category_name = kwargs.pop("category")

        new_tool = ToolModel(**kwargs)
        category = (
            db_session.query(ToolCategoryModel).filter_by(name=category_name).first()
        )

        if not category:
            category = ToolCategoryModel(name=category_name)
            db_session.add(category)

        new_tool.category = category
        db_session.add(new_tool)
        db_session.commit()
        return new_tool


class ToolMutation(ObjectType):
    add_tool = AddTool.Field()
