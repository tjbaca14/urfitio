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
        schema="app"
    )

    op.create_table(
        'feedback',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('user_id', sa.String(), index=True),
        sa.Column('feedback', sa.String(), index=True),
        sa.Column('category', sa.String()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
        schema="app"
    )

    op.create_table(
        'users',
        sa.Column('user_id', sa.String()),
        sa.Column('username', sa.String(), primary_key=True, index=True),
        sa.Column('password_hash', sa.String()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('role', sa.String()),
        sa.Column('tos', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('updated_date', sa.TIMESTAMP(timezone=True), nullable=True),
        schema="priv"
    )
    op.create_table(
        'user_profile',
        sa.Column('user_id', sa.String(), primary_key=True, index=True),
        sa.Column('persona', sa.String()),
        sa.Column('created_date', sa.TIMESTAMP(timezone=True)),
        sa.Column('meta', sa.JSON()),
        schema="priv"

    )

    # Create CoachIndex table in the default schema
    op.create_table(
        'coach_index',
        sa.Column('coach_id', sa.String(), primary_key=True, index=True),
        sa.Column('division', sa.String()),
        sa.Column('data', sa.JSON()),
        schema="app"
    )


def downgrade():
    # Drop tables in reverse order to maintain integrity
    op.drop_table('coach_index', schema="app")
    op.drop_table('chat_history', schema="app")
    op.drop_table('feedback', schema="app")
    op.drop_table('users', schema="priv")
    op.drop_table('user_profile', schema="priv")

