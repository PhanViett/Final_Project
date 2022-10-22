"""UPDATE TABLE thanhPhanHoSo

Revision ID: c0fdd517ec42
Revises: eff7e55fbc9d
Create Date: 2022-06-03 17:16:48.850585

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c0fdd517ec42'
down_revision = 'eff7e55fbc9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_thanh_phan_ho_so',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_tp_ho_so', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lk_thanh_phan_ho_so_thu_tuc',
    sa.Column('thu_tuc_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('thanh_phan_ho_so_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['thanh_phan_ho_so_id'], ['danhmuc_thanh_phan_ho_so.id'], ),
    sa.ForeignKeyConstraint(['thu_tuc_id'], ['danhmuc_thu_tuc.id'], ),
    sa.PrimaryKeyConstraint('thu_tuc_id', 'thanh_phan_ho_so_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_thanh_phan_ho_so_thu_tuc')
    op.drop_table('danhmuc_thanh_phan_ho_so')
    # ### end Alembic commands ###
