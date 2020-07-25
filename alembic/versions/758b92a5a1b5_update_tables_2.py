"""Update tables 2

Revision ID: 758b92a5a1b5
Revises: 15a34a63be96
Create Date: 2020-07-23 16:21:16.431122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "758b92a5a1b5"
down_revision = "15a34a63be96"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tool_category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column(
            "role",
            sa.Enum("BASE", "STUDENT", "NINJA", "FACULTY", "ADMIN", name="role"),
            nullable=True,
        ),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column("class_year", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tool",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["tool_category.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tool_level",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "level",
            sa.Enum("BASIC", "INTERMEDIATE", "CNC", name="traininglevel"),
            nullable=True,
        ),
        sa.Column("tool_id", sa.Integer(), nullable=True),
        sa.Column("prerequisite", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["prerequisite"], ["tool_level.id"],),
        sa.ForeignKeyConstraint(["tool_id"], ["tool.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "training",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("tool_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tool_id"], ["tool.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_tool_level",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tool_id", sa.Integer(), nullable=False),
        sa.Column(
            "tool_level",
            sa.Enum("BASIC", "INTERMEDIATE", "CNC", name="traininglevel"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["tool_id"], ["tool.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("user_id", "tool_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_tool_level")
    op.drop_table("training")
    op.drop_table("tool_level")
    op.drop_table("tool")
    op.drop_table("user")
    op.drop_table("tool_category")
    # ### end Alembic commands ###
