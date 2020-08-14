"""Update models

Revision ID: f601a0b0a36f
Revises: a5c5a68df705
Create Date: 2020-08-14 15:04:16.183681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f601a0b0a36f'
down_revision = 'a5c5a68df705'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tool_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('prerequisite_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prerequisite_id'], ['training.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('BASE', 'STUDENT', 'NINJA', 'FACULTY', 'ADMIN', name='role'), nullable=True),
    sa.Column('display_name', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('class_year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tool',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['tool_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_training',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('STARTED', 'READING', 'WORKSHEET', 'TRAINING', 'TEST_PIECE', 'COMPLETE', name='trainingstatus'), nullable=True),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training_tool',
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.Column('tool_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tool_id'], ['tool.id'], ),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_tool')
    op.drop_table('user_training')
    op.drop_table('tool')
    op.drop_table('user')
    op.drop_table('training')
    op.drop_table('tool_category')
    # ### end Alembic commands ###
