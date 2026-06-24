"""add gamification and badges

Revision ID: 0004_sprint8_gamification
Revises: 0003_add_therapist_fields
Create Date: 2026-06-25 01:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004_sprint8_gamification'
down_revision = '0003_add_therapist_fields'
branch_labels = None
depends_on = None

def upgrade():
    # Add columns to users table
    op.add_column('users', sa.Column('xp', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('level', sa.Integer(), nullable=False, server_default='1'))

    # Create user_badges table
    op.create_table(
        'user_badges',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('badge_id', sa.String(length=50), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'badge_id', name='_user_badge_uc')
    )

def downgrade():
    op.drop_table('user_badges')
    op.drop_column('users', 'level')
    op.drop_column('users', 'xp')
