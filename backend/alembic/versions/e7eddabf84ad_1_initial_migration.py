"""1_Initial_Migration

Revision ID: e7eddabf84ad
Revises: 
Create Date: 2025-10-03 20:26:41.967455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7eddabf84ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_login table
    op.create_table('user_login',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email_id', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False),
        sa.Column('crt_dt', sa.DateTime(), nullable=False),
        sa.Column('crt_by', sa.UUID(), nullable=True),
        sa.Column('lst_updt_dt', sa.DateTime(), nullable=True),
        sa.Column('lst_updt_by', sa.UUID(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_login_email_id'), 'user_login', ['email_id'], unique=True)
    
    # Create user_dtls table
    op.create_table('user_dtls',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('mobile_no', sa.String(length=20), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('email_id', sa.String(length=100), nullable=True),
        sa.Column('blood_grp', sa.String(length=10), nullable=True),
        sa.Column('company_name', sa.String(length=200), nullable=True),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False),
        sa.Column('crt_dt', sa.DateTime(), nullable=False),
        sa.Column('crt_by', sa.UUID(), nullable=True),
        sa.Column('lst_updt_dt', sa.DateTime(), nullable=True),
        sa.Column('lst_updt_by', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_login.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Create qr_dtls table
    op.create_table('qr_dtls',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('first_name', sa.Boolean(), nullable=False),
        sa.Column('last_name', sa.Boolean(), nullable=False),
        sa.Column('mobile_no', sa.Boolean(), nullable=False),
        sa.Column('address', sa.Boolean(), nullable=False),
        sa.Column('email_id', sa.Boolean(), nullable=False),
        sa.Column('blood_grp', sa.Boolean(), nullable=False),
        sa.Column('company_name', sa.Boolean(), nullable=False),
        sa.Column('description', sa.Boolean(), nullable=False),
        sa.Column('active_flag', sa.Boolean(), nullable=False),
        sa.Column('crt_dt', sa.DateTime(), nullable=False),
        sa.Column('crt_by', sa.UUID(), nullable=True),
        sa.Column('lst_updt_dt', sa.DateTime(), nullable=True),
        sa.Column('lst_updt_by', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_login.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create qr_usage table
    op.create_table('qr_usage',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('qr_id', sa.UUID(), nullable=False),
        sa.Column('latitude', sa.String(length=50), nullable=True),
        sa.Column('longitude', sa.String(length=50), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False),
        sa.Column('crt_dt', sa.DateTime(), nullable=False),
        sa.Column('crt_by', sa.UUID(), nullable=True),
        sa.Column('lst_updt_dt', sa.DateTime(), nullable=True),
        sa.Column('lst_updt_by', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['qr_id'], ['qr_dtls.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('qr_usage')
    op.drop_table('qr_dtls')
    op.drop_table('user_dtls')
    op.drop_index(op.f('ix_user_login_email_id'), table_name='user_login')
    op.drop_table('user_login')

