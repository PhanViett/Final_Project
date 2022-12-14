"""UPDATE TABLE cosokinhdoanh properties 

Revision ID: 859c27d985ae
Revises: f1de6634cebf
Create Date: 2022-06-08 09:57:53.209839

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '859c27d985ae'
down_revision = 'f1de6634cebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co_so_kinh_doanh', sa.Column('quan_huyen_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('co_so_kinh_doanh', sa.Column('tinh_thanh_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('co_so_kinh_doanh', sa.Column('xa_phuong_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'co_so_kinh_doanh', 'xa_phuong', ['xa_phuong_id'], ['id'])
    op.create_foreign_key(None, 'co_so_kinh_doanh', 'tinh_thanh', ['tinh_thanh_id'], ['id'])
    op.create_foreign_key(None, 'co_so_kinh_doanh', 'quan_huyen', ['quan_huyen_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'co_so_kinh_doanh', type_='foreignkey')
    op.drop_constraint(None, 'co_so_kinh_doanh', type_='foreignkey')
    op.drop_constraint(None, 'co_so_kinh_doanh', type_='foreignkey')
    op.drop_column('co_so_kinh_doanh', 'xa_phuong_id')
    op.drop_column('co_so_kinh_doanh', 'tinh_thanh_id')
    op.drop_column('co_so_kinh_doanh', 'quan_huyen_id')
    # ### end Alembic commands ###
