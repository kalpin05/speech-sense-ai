"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-31 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated ###
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'therapy_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('expected_text', sa.Text(), nullable=False),
        sa.Column('transcription', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False),
        sa.Column('accuracy_score', sa.Float(), nullable=False),
        sa.Column('fluency_score', sa.String(length=50), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=False),
        sa.Column('audio_file_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated ###
    op.drop_table('therapy_sessions')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
