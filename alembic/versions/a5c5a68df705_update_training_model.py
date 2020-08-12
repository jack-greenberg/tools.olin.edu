"""Update training model

Revision ID: a5c5a68df705
Revises: e632be55513f
Create Date: 2020-08-10 15:21:46.990597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5c5a68df705"
down_revision = "e632be55513f"
branch_labels = None
depends_on = None


training_status_enum = sa.Enum(
    "STARTED",
    "READING",
    "WORKSHEET",
    "TRAINING",
    "TEST_PIECE",
    "COMPLETE",
    name="trainingstatus",
)


def upgrade():
    op.create_table(
        "training_tool",
        sa.Column("training_id", sa.Integer(), nullable=True),
        sa.Column("tool_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tool_id"], ["tool.id"],),
        sa.ForeignKeyConstraint(["training_id"], ["training.id"],),
    )
    op.add_column("training", sa.Column("prerequisite_id", sa.Integer(), nullable=True))
    op.drop_constraint("training_tool_id_fkey", "training", type_="foreignkey")
    op.drop_constraint("training_prerequisite_fkey", "training", type_="foreignkey")
    op.create_foreign_key(None, "training", "training", ["prerequisite_id"], ["id"])
    op.drop_column("training", "tool_id")
    op.drop_column("training", "prerequisite")

    training_status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "user_training", sa.Column("status", training_status_enum, nullable=True,),
    )


def downgrade():
    op.drop_column("user_training", "status")
    training_status_enum.drop(op.get_bind(), checkfirst=True)
    op.add_column(
        "training",
        sa.Column("prerequisite", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "training",
        sa.Column("tool_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "training_prerequisite_fkey", "training", "training", ["prerequisite"], ["id"]
    )
    op.create_foreign_key(
        "training_tool_id_fkey", "training", "tool", ["tool_id"], ["id"]
    )
    op.drop_column("training", "prerequisite_id")
    op.drop_table("training_tool")
