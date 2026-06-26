"""create exercises table

Revision ID: 0005_sprint10_exercises_table
Revises: 0004_sprint8_gamification
Create Date: 2026-06-25 02:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0005_sprint10_exercises_table'
down_revision = '0004_sprint8_gamification'
branch_labels = None
depends_on = None

def upgrade():
    # Drop empty pre-existing table if it exists to avoid program errors
    op.execute("DROP TABLE IF EXISTS exercises CASCADE")

    op.create_table(
        'exercises',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('language', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.String(length=50), server_default='beginner', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('exercises')
