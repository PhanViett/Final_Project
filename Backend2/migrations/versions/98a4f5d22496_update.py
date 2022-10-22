"""update

Revision ID: 98a4f5d22496
Revises: 35791f17773c
Create Date: 2022-05-24 15:15:43.025802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98a4f5d22496'
down_revision = '35791f17773c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_thu_tuc_cchn')
    op.drop_table('lk_nhan_vien_thu_ly_cchn')
    op.drop_table('lk_danh_muc_hoi_dong_cchn')
    op.drop_table('lk_thu_tuc_bo_sung_cchn')
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('nhan_vien_thu_ly_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('thu_tuc_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('thu_tuc_bo_sung_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('hoi_dong_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'yeu_cau_chung_chi_hanh_nghe', 'nhan_vien', ['nhan_vien_thu_ly_id'], ['id'])
    op.create_foreign_key(None, 'yeu_cau_chung_chi_hanh_nghe', 'danhmuc_thu_tuc', ['thu_tuc_id'], ['id'])
    op.create_foreign_key(None, 'yeu_cau_chung_chi_hanh_nghe', 'danhmuc_thu_tuc', ['thu_tuc_bo_sung_id'], ['id'])
    op.create_foreign_key(None, 'yeu_cau_chung_chi_hanh_nghe', 'danhmuc_hoi_dong', ['hoi_dong_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'yeu_cau_chung_chi_hanh_nghe', type_='foreignkey')
    op.drop_constraint(None, 'yeu_cau_chung_chi_hanh_nghe', type_='foreignkey')
    op.drop_constraint(None, 'yeu_cau_chung_chi_hanh_nghe', type_='foreignkey')
    op.drop_constraint(None, 'yeu_cau_chung_chi_hanh_nghe', type_='foreignkey')
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'hoi_dong_id')
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'thu_tuc_bo_sung_id')
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'thu_tuc_id')
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'nhan_vien_thu_ly_id')
    op.create_table('lk_thu_tuc_bo_sung_cchn',
    sa.Column('thu_tuc_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('cchn_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['yeu_cau_chung_chi_hanh_nghe.id'], name='lk_thu_tuc_bo_sung_cchn_cchn_id_fkey'),
    sa.ForeignKeyConstraint(['thu_tuc_id'], ['danhmuc_thu_tuc.id'], name='lk_thu_tuc_bo_sung_cchn_thu_tuc_id_fkey'),
    sa.PrimaryKeyConstraint('thu_tuc_id', 'cchn_id', name='lk_thu_tuc_bo_sung_cchn_pkey')
    )
    op.create_table('lk_danh_muc_hoi_dong_cchn',
    sa.Column('hoi_dong_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('cchn_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['yeu_cau_chung_chi_hanh_nghe.id'], name='lk_danh_muc_hoi_dong_cchn_cchn_id_fkey'),
    sa.ForeignKeyConstraint(['hoi_dong_id'], ['danhmuc_hoi_dong.id'], name='lk_danh_muc_hoi_dong_cchn_hoi_dong_id_fkey'),
    sa.PrimaryKeyConstraint('hoi_dong_id', 'cchn_id', name='lk_danh_muc_hoi_dong_cchn_pkey')
    )
    op.create_table('lk_nhan_vien_thu_ly_cchn',
    sa.Column('nhan_vien_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('cchn_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['yeu_cau_chung_chi_hanh_nghe.id'], name='lk_nhan_vien_thu_ly_cchn_cchn_id_fkey'),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], name='lk_nhan_vien_thu_ly_cchn_nhan_vien_id_fkey'),
    sa.PrimaryKeyConstraint('nhan_vien_id', 'cchn_id', name='lk_nhan_vien_thu_ly_cchn_pkey')
    )
    op.create_table('lk_thu_tuc_cchn',
    sa.Column('thu_tuc_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('cchn_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cchn_id'], ['yeu_cau_chung_chi_hanh_nghe.id'], name='lk_thu_tuc_cchn_cchn_id_fkey'),
    sa.ForeignKeyConstraint(['thu_tuc_id'], ['danhmuc_thu_tuc.id'], name='lk_thu_tuc_cchn_thu_tuc_id_fkey'),
    sa.PrimaryKeyConstraint('thu_tuc_id', 'cchn_id', name='lk_thu_tuc_cchn_pkey')
    )
    # ### end Alembic commands ###
