"""Update table duocsichuacogiayphep

Revision ID: bb11862d485b
Revises: 13f1aa03a022
Create Date: 2022-05-30 13:56:23.940504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bb11862d485b'
down_revision = '13f1aa03a022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('duoc_si_co_so_chua_giay_phep',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ho_ten', sa.String(), nullable=True),
    sa.Column('ngay_sinh', sa.TIMESTAMP(), nullable=True),
    sa.Column('gioi_tinh', sa.String(), nullable=True),
    sa.Column('so_dien_thoai', sa.String(), nullable=True),
    sa.Column('so_nha', sa.String(), nullable=True),
    sa.Column('ten_duong', sa.String(), nullable=True),
    sa.Column('cmnd_cccd', sa.String(), nullable=True),
    sa.Column('bang_cap', sa.String(), nullable=True),
    sa.Column('vi_tri_lam_viec', sa.String(), nullable=True),
    sa.Column('gio_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('xa_phuong_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('quan_huyen_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('tinh_thanh_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('phut_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('gio_ket_thuc', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_ket_thuc', sa.TIMESTAMP(), nullable=True),
    sa.Column('vi_tri_lam_viec_before', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['quan_huyen_id'], ['quan_huyen.id'], ),
    sa.ForeignKeyConstraint(['tinh_thanh_id'], ['tinh_thanh.id'], ),
    sa.ForeignKeyConstraint(['xa_phuong_id'], ['xa_phuong.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('duoc_si_co_so_chua_giay_phep')
    # ### end Alembic commands ###
