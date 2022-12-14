"""UPDATE TABLE yeucaudangkykinhdoanh

Revision ID: cda6ddda26ef
Revises: b444ba993ee7
Create Date: 2022-06-06 17:08:47.760166

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cda6ddda26ef'
down_revision = 'b444ba993ee7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('yeu_cau_dang_ky_kinh_doanh',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('nhan_vien_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ma_ho_so', sa.String(), nullable=True),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ten_co_so', sa.String(), nullable=True),
    sa.Column('ten_co_so_khong_dau', sa.String(), nullable=True),
    sa.Column('loai_yeu_cau', sa.String(), nullable=True),
    sa.Column('thu_tuc_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ma_thu_tuc_bo_sung', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ngay_nop_ho_so', sa.TIMESTAMP(), nullable=True),
    sa.Column('co_quan_cap', sa.String(), nullable=True),
    sa.Column('ngay_cap', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_hieu_luc', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_het_han', sa.TIMESTAMP(), nullable=True),
    sa.Column('lan_cap_thu', sa.String(), nullable=True),
    sa.Column('so_chung_chi_moi', sa.String(), nullable=True),
    sa.Column('loai_ma_chung_chi', sa.String(), nullable=True),
    sa.Column('thay_the_chung_chi', sa.String(), nullable=True),
    sa.Column('hoi_dong_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('so_quyet_dinh', sa.String(), nullable=True),
    sa.Column('ngay_quyet_dinh', sa.TIMESTAMP(), nullable=True),
    sa.Column('loai_ma_chung_chi_gps', sa.String(), nullable=True),
    sa.Column('so_chung_nhan_gps', sa.String(), nullable=True),
    sa.Column('ngay_cap_gps', sa.TIMESTAMP(), nullable=True),
    sa.Column('ngay_het_han_gps', sa.TIMESTAMP(), nullable=True),
    sa.Column('danh_sach_chung_nhan_gps', sa.JSON(), nullable=True),
    sa.Column('danh_sach_chung_nhan_kinh_doanh', sa.JSON(), nullable=True),
    sa.Column('danh_sach_nguoi_hanh_nghe', sa.JSON(), nullable=True),
    sa.Column('ly_do_cap_lai', sa.String(), nullable=True),
    sa.Column('noi_dung_dieu_chinh', sa.String(), nullable=True),
    sa.Column('noi_dung_tham_xet', sa.String(), nullable=True),
    sa.Column('noi_dung_de_nghi', sa.String(), nullable=True),
    sa.Column('noi_dung_yeu_cau', sa.String(), nullable=True),
    sa.Column('ma_nguoi_cap_nhat', sa.String(), nullable=True),
    sa.Column('ten_nguoi_cap_nhat', sa.String(), nullable=True),
    sa.Column('thoi_gian_cap_nhat', sa.TIMESTAMP(), nullable=True),
    sa.Column('ma_nguoi_thu_ly', sa.String(), nullable=True),
    sa.Column('ten_nguoi_thu_ly', sa.String(), nullable=True),
    sa.Column('nguoi_thu_ly', sa.String(), nullable=True),
    sa.Column('y_kien_lanh_dao', sa.String(), nullable=True),
    sa.Column('dinh_kem_don_de_nghi', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_chi_da_cap', sa.String(), nullable=True),
    sa.Column('dinh_kem_cchnd_thay_doi', sa.String(), nullable=True),
    sa.Column('dinh_kem_cndkkdd_gps', sa.String(), nullable=True),
    sa.Column('dinh_kem_so_do_nhansu', sa.String(), nullable=True),
    sa.Column('dinh_kem_so_do_co_so', sa.String(), nullable=True),
    sa.Column('dinh_kem_trang_thiet_bi', sa.String(), nullable=True),
    sa.Column('dinh_kem_ho_so', sa.String(), nullable=True),
    sa.Column('dinh_kem_kiem_tra_thuc_hanh', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_nhan_co_so', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_chi_hanh_nghe', sa.String(), nullable=True),
    sa.Column('dinh_kem_tai_lieu_thuyet_minh', sa.String(), nullable=True),
    sa.Column('dinh_kem_xac_nhan_le_phi', sa.String(), nullable=True),
    sa.Column('dinh_kem_files_khac', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_nhan_bi_sai', sa.String(), nullable=True),
    sa.Column('dinh_kem_ban_sao_cchnd', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_nhan_dang_ky_doanh_nghiep', sa.String(), nullable=True),
    sa.Column('dinh_kem_chung_nhan_da_cap', sa.String(), nullable=True),
    sa.Column('ly_do_tu_choi', sa.String(), nullable=True),
    sa.Column('ma_nguoi_tu_choi', sa.String(), nullable=True),
    sa.Column('ten_nguoi_tu_choi', sa.String(), nullable=True),
    sa.Column('thoi_gian_tu_choi', sa.String(), nullable=True),
    sa.Column('thoi_gian_thu_ly', sa.String(), nullable=True),
    sa.Column('ngay_het_han_ho_so', sa.String(), nullable=True),
    sa.Column('thoi_gian_nop_ho_so', sa.String(), nullable=True),
    sa.Column('thoi_gian_in_du_thao', sa.String(), nullable=True),
    sa.Column('thoi_gian_in_tham_xet', sa.String(), nullable=True),
    sa.Column('thoi_gian_in_chung_chi', sa.String(), nullable=True),
    sa.Column('thoi_gian_lanh_dao_duyet', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.String(), nullable=True),
    sa.Column('so_dan_chieu', sa.String(), nullable=True),
    sa.Column('ket_qua_tham_xet', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['hoi_dong_id'], ['danhmuc_hoi_dong.id'], ),
    sa.ForeignKeyConstraint(['ma_thu_tuc_bo_sung'], ['danhmuc_thu_tuc.id'], ),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], ),
    sa.ForeignKeyConstraint(['thu_tuc_id'], ['danhmuc_thu_tuc.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lk_loai_hinh_dang_ky_kinh_doanh',
    sa.Column('danhmuc_loai_hinh_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_loai_hinh_kinh_doanh_id'], ['danhmuc_loai_hinh_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], ),
    sa.PrimaryKeyConstraint('danhmuc_loai_hinh_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id')
    )
    op.create_table('lk_pham_vi_dang_ky_kinh_doanh',
    sa.Column('danhmuc_pham_vi_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_pham_vi_kinh_doanh_id'], ['danhmuc_pham_vi_hoat_dong_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], ),
    sa.PrimaryKeyConstraint('danhmuc_pham_vi_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_pham_vi_dang_ky_kinh_doanh')
    op.drop_table('lk_loai_hinh_dang_ky_kinh_doanh')
    op.drop_table('yeu_cau_dang_ky_kinh_doanh')
    # ### end Alembic commands ###
