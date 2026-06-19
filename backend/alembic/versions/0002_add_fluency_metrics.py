"""add fluency metrics

Revision ID: 0002_add_fluency_metrics
Revises: 0001_initial
Create Date: 2026-06-19 15:45:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_fluency_metrics'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('therapy_sessions', sa.Column('fluency_score_val', sa.Integer(), nullable=True))
    op.add_column('therapy_sessions', sa.Column('speech_rate', sa.Integer(), nullable=True))
    op.add_column('therapy_sessions', sa.Column('pause_count', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('therapy_sessions', 'pause_count')
    op.drop_column('therapy_sessions', 'speech_rate')
    op.drop_column('therapy_sessions', 'fluency_score_val')
