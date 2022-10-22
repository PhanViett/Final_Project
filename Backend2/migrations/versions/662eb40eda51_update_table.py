"""update Table 

Revision ID: 662eb40eda51
Revises: f0edf813be54
Create Date: 2022-05-13 11:09:29.935426

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '662eb40eda51'
down_revision = 'f0edf813be54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lich_su_dao_tao',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('nhan_vien_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ma_chuong_trinh', sa.String(), nullable=True),
    sa.Column('ten_chuong_trinh', sa.String(), nullable=True),
    sa.Column('tu_ngay', sa.TIMESTAMP(), nullable=True),
    sa.Column('den_ngay', sa.TIMESTAMP(), nullable=True),
    sa.Column('quy_doi_so_gio', sa.String(), nullable=True),
    sa.Column('noi_dung_chuyen_mon', sa.String(), nullable=True),
    sa.Column('chung_tu_dinh_kem', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('thoi_gian_duyet', sa.TIMESTAMP(), nullable=True),
    sa.Column('ten_truong', sa.String(), nullable=True),
    sa.Column('so_GCN_dao_tao', sa.String(), nullable=True),
    sa.Column('ngay_cap_GCN', sa.TIMESTAMP(), nullable=True),
    sa.Column('so_tiet_hoc', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lich_su_dao_tao')
    # ### end Alembic commands ###
