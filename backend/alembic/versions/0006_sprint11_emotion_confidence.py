"""add emotion and confidence columns to therapy sessions

Revision ID: 0006_sprint11_emotion_confidence
Revises: 0005_sprint10_exercises_table
Create Date: 2026-07-04 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0006_sprint11_emotion_confidence'
down_revision = '0005_sprint10_exercises_table'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('therapy_sessions', sa.Column('confidence_score', sa.Float(), nullable=True))
    op.add_column('therapy_sessions', sa.Column('nervousness_score', sa.Float(), nullable=True))
    op.add_column('therapy_sessions', sa.Column('hesitation_score', sa.Float(), nullable=True))
    op.add_column('therapy_sessions', sa.Column('emotion', sa.String(length=50), nullable=True))

def downgrade():
    op.drop_column('therapy_sessions', 'emotion')
    op.drop_column('therapy_sessions', 'hesitation_score')
    op.drop_column('therapy_sessions', 'nervousness_score')
    op.drop_column('therapy_sessions', 'confidence_score')
