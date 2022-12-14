"""empty message

Revision ID: 43f4f97e74c1
Revises: 
Create Date: 2022-10-16 18:13:21.950212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43f4f97e74c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('deactive_at', sa.BigInteger(), nullable=True),
    sa.Column('delete_at', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ho', sa.String(length=80), nullable=True),
    sa.Column('ten', sa.String(length=80), nullable=True),
    sa.Column('ho_ten', sa.String(length=80), nullable=True),
    sa.Column('ten_khong_dau', sa.String(length=80), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('ngay_sinh', sa.BigInteger(), nullable=True),
    sa.Column('gioi_tinh', sa.String(), nullable=True),
    sa.Column('dien_thoai', sa.String(length=12), nullable=True),
    sa.Column('ma_cong_dan', sa.String(length=80), nullable=True),
    sa.Column('ngay_cap', sa.BigInteger(), nullable=True),
    sa.Column('noi_cap', sa.String(length=80), nullable=True),
    sa.Column('dia_chi', sa.String(), nullable=True),
    sa.Column('so_nha', sa.String(), nullable=True),
    sa.Column('vai_tro', sa.String(), nullable=False),
    sa.Column('tai_khoan', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predicts',
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('result', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('predicts')
    op.drop_table('users')
    # ### end Alembic commands ###
