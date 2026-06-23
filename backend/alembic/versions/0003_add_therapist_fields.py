"""add therapist fields

Revision ID: 0003_add_therapist_fields
Revises: 0002_add_fluency_metrics
Create Date: 2026-06-23 22:50:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003_add_therapist_fields'
down_revision = '0002_add_fluency_metrics'
branch_labels = None
depends_on = None

def upgrade():
    # Add columns to users table
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=False, server_default='patient'))
    op.add_column('users', sa.Column('therapist_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        'fk_users_therapist_id',
        source_table='users',
        referent_table='users',
        local_cols=['therapist_id'],
        remote_cols=['id'],
        ondelete='SET NULL'
    )

def downgrade():
    op.drop_constraint('fk_users_therapist_id', 'users', type_='foreignkey')
    op.drop_column('users', 'therapist_id')
    op.drop_column('users', 'role')
