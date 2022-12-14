"""update

Revision ID: daec71fdcc55
Revises: 7871b20b9e99
Create Date: 2022-05-11 14:55:12.462308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'daec71fdcc55'
down_revision = '7871b20b9e99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('noi_dung_thuc_hanh',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_noi_dung_thuc_hanh', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('danhmuc_thanh_phan_ho_so')
    op.drop_table('danhmuc_van_bang_chuyen_mon')
    op.drop_table('danhmuc_pham_vi_hoat_dong_kinh_doanh')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_pham_vi_hoat_dong_kinh_doanh',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ma_hoat_dong_kinh_doanh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_khong_dau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('trang_thai', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='danhmuc_pham_vi_hoat_dong_kinh_doanh_pkey')
    )
    op.create_table('danhmuc_van_bang_chuyen_mon',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ma_chuyen_mon', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_khong_dau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('trang_thai', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='danhmuc_van_bang_chuyen_mon_pkey')
    )
    op.create_table('danhmuc_thanh_phan_ho_so',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ma_tp_ho_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_khong_dau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ma_thu_tuc', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('trang_thai', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='danhmuc_thanh_phan_ho_so_pkey')
    )
    op.drop_table('noi_dung_thuc_hanh')
    # ### end Alembic commands ###
