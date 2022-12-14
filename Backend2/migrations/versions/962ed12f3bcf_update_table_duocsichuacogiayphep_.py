"""Update table duocsichuacogiayphep diachi,xp,qh

Revision ID: 962ed12f3bcf
Revises: d657872b6db3
Create Date: 2022-05-30 14:10:28.987895

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '962ed12f3bcf'
down_revision = 'd657872b6db3'
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
    sa.Column('cmnd_cccd', sa.String(), nullable=True),
    sa.Column('bang_cap', sa.String(), nullable=True),
    sa.Column('vi_tri_lam_viec', sa.String(), nullable=True),
    sa.Column('gio_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('dia_chi', sa.String(), nullable=True),
    sa.Column('phut_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('gio_ket_thuc', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_bat_dau', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_ket_thuc', sa.TIMESTAMP(), nullable=True),
    sa.Column('vi_tri_lam_viec_before', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('duoc_si_co_so_chua_giay_phep')
    # ### end Alembic commands ###
