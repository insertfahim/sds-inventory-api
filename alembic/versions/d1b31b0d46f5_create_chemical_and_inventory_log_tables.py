"""Create chemical and inventory_log tables

Revision ID: d1b31b0d46f5
Revises: 
Create Date: 2025-09-06 04:43:59.381454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1b31b0d46f5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create chemicals table
    op.create_table('chemicals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('cas_number', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chemicals_id'), 'chemicals', ['id'], unique=False)
    
    # Create inventory_logs table
    op.create_table('inventory_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chemical_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['chemical_id'], ['chemicals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_logs_id'), 'inventory_logs', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_inventory_logs_id'), table_name='inventory_logs')
    op.drop_table('inventory_logs')
    op.drop_index(op.f('ix_chemicals_id'), table_name='chemicals')
    op.drop_table('chemicals')
