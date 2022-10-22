"""UPDATE TABLE duocsicosochuagiayphep  properties 

Revision ID: ba397a316f18
Revises: 859c27d985ae
Create Date: 2022-06-08 10:05:44.443807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ba397a316f18'
down_revision = '859c27d985ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('duoc_si_co_so_chua_giay_phep', sa.Column('quan_huyen_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('duoc_si_co_so_chua_giay_phep', sa.Column('tinh_thanh_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('duoc_si_co_so_chua_giay_phep', sa.Column('xa_phuong_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'duoc_si_co_so_chua_giay_phep', 'quan_huyen', ['quan_huyen_id'], ['id'])
    op.create_foreign_key(None, 'duoc_si_co_so_chua_giay_phep', 'tinh_thanh', ['tinh_thanh_id'], ['id'])
    op.create_foreign_key(None, 'duoc_si_co_so_chua_giay_phep', 'xa_phuong', ['xa_phuong_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'duoc_si_co_so_chua_giay_phep', type_='foreignkey')
    op.drop_constraint(None, 'duoc_si_co_so_chua_giay_phep', type_='foreignkey')
    op.drop_constraint(None, 'duoc_si_co_so_chua_giay_phep', type_='foreignkey')
    op.drop_column('duoc_si_co_so_chua_giay_phep', 'xa_phuong_id')
    op.drop_column('duoc_si_co_so_chua_giay_phep', 'tinh_thanh_id')
    op.drop_column('duoc_si_co_so_chua_giay_phep', 'quan_huyen_id')
    # ### end Alembic commands ###
