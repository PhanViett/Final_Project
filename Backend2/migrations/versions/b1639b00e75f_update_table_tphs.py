"""UPDATE TABLE TPHS

Revision ID: b1639b00e75f
Revises: 0afad9526c0b
Create Date: 2022-06-03 15:16:29.840277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1639b00e75f'
down_revision = '0afad9526c0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_thanh_phan_ho_so',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_tp_ho_so', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('ma_thu_tuc', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['ma_thu_tuc'], ['danhmuc_thu_tuc.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('danhmuc_thanh_phan_ho_so')
    # ### end Alembic commands ###
