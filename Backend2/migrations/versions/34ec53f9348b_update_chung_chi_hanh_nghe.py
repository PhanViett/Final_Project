"""update chung chi hanh nghe

Revision ID: 34ec53f9348b
Revises: 1cc0ee44b660
Create Date: 2022-05-23 13:30:27.433011

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34ec53f9348b'
down_revision = '1cc0ee44b660'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chung_chi_hanh_nghe',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('nhan_vien_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('thoi_gian_yeu_cau_lien_ket', sa.TIMESTAMP(), nullable=True),
    sa.Column('thoi_gian_duyet_lien_ket', sa.TIMESTAMP(), nullable=True),
    sa.Column('thoi_gian_tu_choi_lien_ket', sa.TIMESTAMP(), nullable=True),
    sa.Column('ly_do_tu_choi', sa.TEXT(), nullable=True),
    sa.Column('nguoi_duyet_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('so_giay_phep', sa.String(), nullable=True),
    sa.Column('co_quan_cap', sa.String(), nullable=True),
    sa.Column('ngay_hieu_luc', sa.TIMESTAMP(), nullable=True),
    sa.Column('nam_cap', sa.String(), nullable=True),
    sa.Column('noi_cong_tac', sa.String(), nullable=True),
    sa.Column('dia_chi_cong_tac', sa.String(), nullable=True),
    sa.Column('loai_cap_chung_chi', sa.String(), nullable=True),
    sa.Column('hinh_thuc', sa.String(), nullable=True),
    sa.Column('noi_dung_dieu_chinh', sa.TEXT(), nullable=True),
    sa.Column('lan_cap_thu', sa.String(), nullable=True),
    sa.Column('thay_the_chung_chi', sa.String(), nullable=True),
    sa.Column('yeu_cau_phien_dich', sa.Boolean(), nullable=True),
    sa.Column('so_quyet_dinh', sa.String(), nullable=True),
    sa.Column('ngay_quyet_dinh', sa.TIMESTAMP(), nullable=True),
    sa.Column('dinh_kem_chung_chi', sa.String(), nullable=True),
    sa.Column('dinh_kem_don_de_nghi', sa.String(), nullable=True),
    sa.Column('dinh_kem_anh_chan_dung', sa.String(), nullable=True),
    sa.Column('dinh_kem_van_bang_chuyen_mon', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_suc_khoe', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_thuc_hanh', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_dao_tao', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_cong_dan', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_ly_lich', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_cam_ket', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_le_phi', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_thay_doi', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_khac', sa.String(), nullable=True),
    sa.Column('trang_thai_ho_so', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['nguoi_duyet_id'], ['nhan_vien.id'], ),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lk_pham_vi_chuyen_mon_cchn',
    sa.Column('pham_vi_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cchn_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['chung_chi_hanh_nghe.id'], ),
    sa.ForeignKeyConstraint(['pham_vi_id'], ['danhmuc_pham_vi_hoat_dong_chuyen_mon.id'], ),
    sa.PrimaryKeyConstraint('pham_vi_id', 'cchn_id')
    )
    op.create_table('lk_van_bang_chuyen_mon_cchn',
    sa.Column('van_bang_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cchn_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['chung_chi_hanh_nghe.id'], ),
    sa.ForeignKeyConstraint(['van_bang_id'], ['danhmuc_van_bang_chuyen_mon.id'], ),
    sa.PrimaryKeyConstraint('van_bang_id', 'cchn_id')
    )
    op.create_table('lk_vi_tri_hanh_nghe_cchn',
    sa.Column('vi_tri_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cchn_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['chung_chi_hanh_nghe.id'], ),
    sa.ForeignKeyConstraint(['vi_tri_id'], ['danhmuc_vi_tri_hanh_nghe.id'], ),
    sa.PrimaryKeyConstraint('vi_tri_id', 'cchn_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_vi_tri_hanh_nghe_cchn')
    op.drop_table('lk_van_bang_chuyen_mon_cchn')
    op.drop_table('lk_pham_vi_chuyen_mon_cchn')
    op.drop_table('chung_chi_hanh_nghe')
    # ### end Alembic commands ###
