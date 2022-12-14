"""Update data table

Revision ID: df4f194b0d92
Revises: 05dc96b27f8b
Create Date: 2022-07-20 14:13:33.254884

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'df4f194b0d92'
down_revision = '05dc96b27f8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('lich_su_chung_chi_quan_huyen_id_fkey', 'lich_su_chung_chi', type_='foreignkey')
    op.drop_constraint('lich_su_chung_chi_tinh_thanh_id_fkey', 'lich_su_chung_chi', type_='foreignkey')
    op.drop_constraint('lich_su_chung_chi_xa_phuong_id_fkey', 'lich_su_chung_chi', type_='foreignkey')
    op.drop_column('lich_su_chung_chi', 'tinh_thanh_id')
    op.drop_column('lich_su_chung_chi', 'quan_huyen_id')
    op.drop_column('lich_su_chung_chi', 'xa_phuong_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lich_su_chung_chi', sa.Column('xa_phuong_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('lich_su_chung_chi', sa.Column('quan_huyen_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('lich_su_chung_chi', sa.Column('tinh_thanh_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('lich_su_chung_chi_xa_phuong_id_fkey', 'lich_su_chung_chi', 'xa_phuong', ['xa_phuong_id'], ['id'])
    op.create_foreign_key('lich_su_chung_chi_tinh_thanh_id_fkey', 'lich_su_chung_chi', 'tinh_thanh', ['tinh_thanh_id'], ['id'])
    op.create_foreign_key('lich_su_chung_chi_quan_huyen_id_fkey', 'lich_su_chung_chi', 'quan_huyen', ['quan_huyen_id'], ['id'])
    # ### end Alembic commands ###
