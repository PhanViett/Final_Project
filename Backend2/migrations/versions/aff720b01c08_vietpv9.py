"""vietpv9

Revision ID: aff720b01c08
Revises: bf7bbec6cb64
Create Date: 2022-08-24 10:10:56.290667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aff720b01c08'
down_revision = 'bf7bbec6cb64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lk_loai_hinh_kinh_doanh',
    sa.Column('loai_hinh_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['loai_hinh_kinh_doanh_id'], ['danhmuc_loai_hinh_kinh_doanh.id'], ),
    sa.PrimaryKeyConstraint('loai_hinh_kinh_doanh_id', 'co_so_kinh_doanh_id')
    )
    op.create_table('lk_pham_vi_kinh_doanh',
    sa.Column('pham_vi_hoat_dong_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('co_so_kinh_doanh_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['co_so_kinh_doanh_id'], ['co_so_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['pham_vi_hoat_dong_kinh_doanh_id'], ['danhmuc_pham_vi_hoat_dong_kinh_doanh.id'], ),
    sa.PrimaryKeyConstraint('pham_vi_hoat_dong_kinh_doanh_id', 'co_so_kinh_doanh_id')
    )
    op.create_table('lk_vai_tro_to_chuc',
    sa.Column('vai_tro_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('to_chuc_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['to_chuc_id'], ['co_so_kinh_doanh.id'], ),
    sa.ForeignKeyConstraint(['vai_tro_id'], ['vai_tro.id'], ),
    sa.PrimaryKeyConstraint('vai_tro_id', 'to_chuc_id')
    )
    op.drop_table('lk_loai_hinh_dang_ky_kinh_doanh')
    op.drop_table('lk_pham_vi_dang_ky_kinh_doanh')
    op.add_column('co_so_kinh_doanh', sa.Column('ngay_cap', sa.BigInteger(), nullable=True))
    op.add_column('danhmuc_vi_tri_hanh_nghe', sa.Column('loai', sa.String(), nullable=False))
    op.add_column('yeu_cau_dang_ky_kinh_doanh', sa.Column('doi_tuong', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('yeu_cau_dang_ky_kinh_doanh', sa.Column('pham_vi_kinh_doanh', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('yeu_cau_dang_ky_kinh_doanh', 'pham_vi_kinh_doanh')
    op.drop_column('yeu_cau_dang_ky_kinh_doanh', 'doi_tuong')
    op.drop_column('danhmuc_vi_tri_hanh_nghe', 'loai')
    op.drop_column('co_so_kinh_doanh', 'ngay_cap')
    op.create_table('lk_pham_vi_dang_ky_kinh_doanh',
    sa.Column('danhmuc_pham_vi_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_pham_vi_kinh_doanh_id'], ['danhmuc_pham_vi_hoat_dong_kinh_doanh.id'], name='lk_pham_vi_dang_ky_kinh_doanh_danhmuc_pham_vi_kinh_doanh_i_fkey'),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], name='lk_pham_vi_dang_ky_kinh_doanh_yeu_cau_dang_ky_kinh_doanh_i_fkey'),
    sa.PrimaryKeyConstraint('danhmuc_pham_vi_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id', name='lk_pham_vi_dang_ky_kinh_doanh_pkey')
    )
    op.create_table('lk_loai_hinh_dang_ky_kinh_doanh',
    sa.Column('danhmuc_loai_hinh_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('yeu_cau_dang_ky_kinh_doanh_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['danhmuc_loai_hinh_kinh_doanh_id'], ['danhmuc_loai_hinh_kinh_doanh.id'], name='lk_loai_hinh_dang_ky_kinh_doa_danhmuc_loai_hinh_kinh_doanh_fkey'),
    sa.ForeignKeyConstraint(['yeu_cau_dang_ky_kinh_doanh_id'], ['yeu_cau_dang_ky_kinh_doanh.id'], name='lk_loai_hinh_dang_ky_kinh_doa_yeu_cau_dang_ky_kinh_doanh_i_fkey'),
    sa.PrimaryKeyConstraint('danhmuc_loai_hinh_kinh_doanh_id', 'yeu_cau_dang_ky_kinh_doanh_id', name='lk_loai_hinh_dang_ky_kinh_doanh_pkey')
    )
    op.drop_table('lk_vai_tro_to_chuc')
    op.drop_table('lk_pham_vi_kinh_doanh')
    op.drop_table('lk_loai_hinh_kinh_doanh')
    # ### end Alembic commands ###