"""Update models

Revision ID: f601a0b0a36f
Revises: a5c5a68df705
Create Date: 2020-08-14 15:04:16.183681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f601a0b0a36f"
down_revision = "a5c5a68df705"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
    #  op.drop_table("training_tool")
    #  op.drop_table("user_training")
    #  op.drop_table("tool")
    #  op.drop_table("user")
    #  op.drop_table("training")
    #  op.drop_table("tool_category")
