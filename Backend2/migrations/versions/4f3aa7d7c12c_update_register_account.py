"""update register account

Revision ID: 4f3aa7d7c12c
Revises: fb96e6607bba
Create Date: 2022-05-10 13:38:38.116080

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4f3aa7d7c12c'
down_revision = 'fb96e6607bba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('danhmuc_noi_tot_nghiep')
    op.add_column('tai_khoan', sa.Column('dien_thoai', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tai_khoan', 'dien_thoai')
    op.create_table('danhmuc_noi_tot_nghiep',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ma_noi_tot_nghiep', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ten_khong_dau', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('trang_thai', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='danhmuc_noi_tot_nghiep_pkey')
    )
    # ### end Alembic commands ###
