"""Update data table

Revision ID: 497e05a94c17
Revises: 4bff2129dbe5
Create Date: 2022-06-20 09:36:39.122317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '497e05a94c17'
down_revision = '4bff2129dbe5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loai_ma_chung_chi',
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_chung_chi', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('so_da_cap', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loai_magps',
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_gps', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('so_da_cap', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loai_magps')
    op.drop_table('loai_ma_chung_chi')
    # ### end Alembic commands ###