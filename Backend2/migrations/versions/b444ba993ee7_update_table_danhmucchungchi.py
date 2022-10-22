"""UPDATE TABLE DanhMucChungChi

Revision ID: b444ba993ee7
Revises: ead0a16212e3
Create Date: 2022-06-06 14:10:49.567986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b444ba993ee7'
down_revision = 'ead0a16212e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_pham_vi_dang_ky_kinh_doanh')
    op.drop_table('lk_loai_hinh_dang_ky_kinh_doanh')
    op.drop_table('yeu_cau_dang_ky_kinh_doanh')
    op.drop_table('duoc_si_co_so_chua_giay_phep')
    op.add_column('duoc_si_co_so', sa.Column('chung_chi_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.drop_constraint('duoc_si_co_so_chung_chi_hanh_nghe_id_fkey', 'duoc_si_co_so', type_='foreignkey')
    op.create_foreign_key(None, 'duoc_si_co_so', 'danhmuc_chung_chi', ['chung_chi_id'], ['id'])
    op.drop_column('duoc_si_co_so', 'chung_chi_hanh_nghe_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('duoc_si_co_so', sa.Column('chung_chi_hanh_nghe_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'duoc_si_co_so', type_='foreignkey')
    op.create_foreign_key('duoc_si_co_so_chung_chi_hanh_nghe_id_fkey', 'duoc_si_co_so', 'danhmuc_chung_chi', ['chung_chi_hanh_nghe_id'], ['id'])
    op.drop_column('duoc_si_co_so', 'chung_chi_id')
    op.create_table('duoc_si_co_so_chua_giay_phep',
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('deleted_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ho_ten', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ngay_sinh', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('gioi_tinh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('so_dien_thoai', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cmnd_cccd', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('bang_cap', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('vi_tri_lam_viec', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('gio_bat_dau', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('dia_chi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phut_bat_dau', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('gio_ket_thuc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_bat_dau', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_ket_thuc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('vi_tri_lam_viec_before', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], name='duoc_si_co_so_chua_giay_phep_co_so_kinh_doanh_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='duoc_si_co_so_chua_giay_phep_pkey')
    )
    op.create_table('yeu_cau_dang_ky_kinh_doanh',
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('deleted_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('nhan_vien_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('ma_ho_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('ten_co_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_co_so_khong_dau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('loai_yeu_cau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('thu_tuc_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('ma_thu_tuc_bo_sung', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('ngay_nop_ho_so', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('co_quan_cap', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ngay_cap', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_hieu_luc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_het_han', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('lan_cap_thu', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('so_chung_chi_moi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('loai_ma_chung_chi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('thay_the_chung_chi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hoi_dong_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('so_quyet_dinh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ngay_quyet_dinh', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('loai_ma_chung_chi_gps', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('so_chung_nhan_gps', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ngay_cap_gps', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_het_han_gps', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('danh_sach_chung_nhan_gps', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('danh_sach_chung_nhan_kinh_doanh', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('danh_sach_nguoi_hanh_nghe', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('ly_do_cap_lai', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('noi_dung_dieu_chinh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('noi_dung_tham_xet', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('noi_dung_de_nghi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('noi_dung_yeu_cau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ma_nguoi_cap_nhat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_nguoi_cap_nhat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_cap_nhat', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ma_nguoi_thu_ly', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_nguoi_thu_ly', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('nguoi_thu_ly', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('y_kien_lanh_dao', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_don_de_nghi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_chi_da_cap', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_cchnd_thay_doi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_cndkkdd_gps', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_so_do_nhansu', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_so_do_co_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_trang_thiet_bi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_ho_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_kiem_tra_thuc_hanh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_nhan_co_so', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_chi_hanh_nghe', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_tai_lieu_thuyet_minh', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_xac_nhan_le_phi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_files_khac', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_nhan_bi_sai', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_ban_sao_cchnd', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_nhan_dang_ky_doanh_nghiep', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dinh_kem_chung_nhan_da_cap', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ly_do_tu_choi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ma_nguoi_tu_choi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_nguoi_tu_choi', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_tu_choi', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_thu_ly', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('ngay_het_han_ho_so', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_nop_ho_so', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_in_du_thao', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_in_tham_xet', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_in_chung_chi', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('thoi_gian_lanh_dao_duyet', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('trang_thai', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('so_dan_chieu', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ket_qua_tham_xet', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], name='yeu_cau_dang_ky_kinh_doanh_co_so_kinh_doanh_id_fkey'),
    sa.ForeignKeyConstraint(['hoi_dong_id'], ['danhmuc_hoi_dong.id'], name='yeu_cau_dang_ky_kinh_doanh_hoi_dong_id_fkey'),
    sa.ForeignKeyConstraint(['ma_thu_tuc_bo_sung'], ['danhmuc_thu_tuc.id'], name='yeu_cau_dang_ky_kinh_doanh_ma_thu_tuc_bo_sung_fkey'),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], name='yeu_cau_dang_ky_kinh_doanh_nhan_vien_id_fkey'),
    sa.ForeignKeyConstraint(['thu_tuc_id'], ['danhmuc_thu_tuc.id'], name='yeu_cau_dang_ky_kinh_doanh_thu_tuc_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='yeu_cau_dang_ky_kinh_doanh_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('lk_loai_hinh_dang_ky_kinh_doanh',
    sa.Column('danhmuc_loai_hinh_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_loai_hinh_kinh_doanh_id'], ['danhmuc_loai_hinh_kinh_doanh.id'], name='lk_loai_hinh_dang_ky_kinh_doa_danhmuc_loai_hinh_kinh_doanh_fkey'),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], name='lk_loai_hinh_dang_ky_kinh_doa_yeu_cau_dang_ky_kinh_doanh_i_fkey'),
    sa.PrimaryKeyConstraint('danhmuc_loai_hinh_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id', name='lk_loai_hinh_dang_ky_kinh_doanh_pkey')
    )
    op.create_table('lk_pham_vi_dang_ky_kinh_doanh',
    sa.Column('danhmuc_pham_vi_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_pham_vi_kinh_doanh_id'], ['danhmuc_pham_vi_hoat_dong_kinh_doanh.id'], name='lk_pham_vi_dang_ky_kinh_doanh_danhmuc_pham_vi_kinh_doanh_i_fkey'),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], name='lk_pham_vi_dang_ky_kinh_doanh_yeu_cau_dang_ky_kinh_doanh_i_fkey'),
    sa.PrimaryKeyConstraint('danhmuc_pham_vi_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id', name='lk_pham_vi_dang_ky_kinh_doanh_pkey')
    )
    # ### end Alembic commands ###
