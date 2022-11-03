"""Update data table

Revision ID: 06bdacab4599
Revises: 35445c1908e8
Create Date: 2022-07-20 09:45:52.012491

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '06bdacab4599'
down_revision = '35445c1908e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lich_su_chung_chi', sa.Column('quan_huyen_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('lich_su_chung_chi', sa.Column('tinh_thanh_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('lich_su_chung_chi', sa.Column('xa_phuong_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('lich_su_chung_chi', sa.Column('vai_tro_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'lich_su_chung_chi', 'tinh_thanh', ['tinh_thanh_id'], ['id'])
    op.create_foreign_key(None, 'lich_su_chung_chi', 'vai_tro', ['vai_tro_id'], ['id'])
    op.create_foreign_key(None, 'lich_su_chung_chi', 'quan_huyen', ['quan_huyen_id'], ['id'])
    op.create_foreign_key(None, 'lich_su_chung_chi', 'xa_phuong', ['xa_phuong_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'lich_su_chung_chi', type_='foreignkey')
    op.drop_constraint(None, 'lich_su_chung_chi', type_='foreignkey')
    op.drop_constraint(None, 'lich_su_chung_chi', type_='foreignkey')
    op.drop_constraint(None, 'lich_su_chung_chi', type_='foreignkey')
    op.drop_column('lich_su_chung_chi', 'vai_tro_id')
    op.drop_column('lich_su_chung_chi', 'xa_phuong_id')
    op.drop_column('lich_su_chung_chi', 'tinh_thanh_id')
    op.drop_column('lich_su_chung_chi', 'quan_huyen_id')
    # ### end Alembic commands ###