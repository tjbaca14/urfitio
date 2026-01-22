"""create initial tables

Revision ID: 575608f97d40
Revises: 
Create Date: 2025-01-12 23:53:33.147873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '575608f97d40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'chat_history',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('user_id', sa.String(), index=True),
        sa.Column('messages', sa.JSON()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_date', sa.TIMESTAMP(timezone=True)),
    )

    op.create_table(
        'feedback',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('user_id', sa.String(), index=True),
        sa.Column('feedback', sa.String(), index=True),
        sa.Column('category', sa.String()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
    )

    op.create_table(
        'division',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('division_type', sa.String(), nullable=False)
    )

    op.create_table(
        'school',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('division_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('context', sa.String()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
        # Foreign key constraint
        sa.ForeignKeyConstraint(['division_id'], ['division.id'], ondelete='CASCADE'),
    )


def downgrade():
    op.drop_table('school')
    op.drop_table('division')
    op.drop_table('feedback')
    op.drop_table('chat_history')