"""create table danhmuc_vi_tri_hanh_nghe

Revision ID: 7871b20b9e99
Revises: 2c98c7ac93e3
Create Date: 2022-05-10 16:44:29.588192

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7871b20b9e99'
down_revision = '2c98c7ac93e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_noi_tot_nghiep',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_noi_tot_nghiep', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('danhmuc_vi_tri_hanh_nghe',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_hanh_nghe', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('rut_gon', sa.String(), nullable=True),
    sa.Column('loai', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('danhmuc_vi_tri_hanh_nghe')
    op.drop_table('danhmuc_noi_tot_nghiep')
    # ### end Alembic commands ###
