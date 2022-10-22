"""UPDATE TABLE 

Revision ID: f1de6634cebf
Revises: 8b28b79474d3
Create Date: 2022-06-08 09:55:14.303709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1de6634cebf'
down_revision = '8b28b79474d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chung_nhan_thuc_hanh_co_so', sa.Column('quan_huyen_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('chung_nhan_thuc_hanh_co_so', sa.Column('tinh_thanh_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('chung_nhan_thuc_hanh_co_so', sa.Column('xa_phuong_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'chung_nhan_thuc_hanh_co_so', 'quan_huyen', ['quan_huyen_id'], ['id'])
    op.create_foreign_key(None, 'chung_nhan_thuc_hanh_co_so', 'xa_phuong', ['xa_phuong_id'], ['id'])
    op.create_foreign_key(None, 'chung_nhan_thuc_hanh_co_so', 'tinh_thanh', ['tinh_thanh_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chung_nhan_thuc_hanh_co_so', type_='foreignkey')
    op.drop_constraint(None, 'chung_nhan_thuc_hanh_co_so', type_='foreignkey')
    op.drop_constraint(None, 'chung_nhan_thuc_hanh_co_so', type_='foreignkey')
    op.drop_column('chung_nhan_thuc_hanh_co_so', 'xa_phuong_id')
    op.drop_column('chung_nhan_thuc_hanh_co_so', 'tinh_thanh_id')
    op.drop_column('chung_nhan_thuc_hanh_co_so', 'quan_huyen_id')
    # ### end Alembic commands ###
