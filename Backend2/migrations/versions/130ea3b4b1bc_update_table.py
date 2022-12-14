"""update Table 

Revision ID: 130ea3b4b1bc
Revises: 7bac9cb8cbd1
Create Date: 2022-05-12 09:49:23.588815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '130ea3b4b1bc'
down_revision = '7bac9cb8cbd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_hoi_dong',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_hoi_dong', sa.String(), nullable=True),
    sa.Column('ten_hoi_dong', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('ngay_thanh_lap', sa.TIMESTAMP(), nullable=True),
    sa.Column('ten_nguoi_phu_trach', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('danhmuc_hoi_dong')
    # ### end Alembic commands ###
