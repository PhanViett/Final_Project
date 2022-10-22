"""create table danhmuc_van_bang_chuyen_mon

Revision ID: 2eef26aa261b
Revises: e700d1378fc5
Create Date: 2022-05-11 09:27:20.290315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2eef26aa261b'
down_revision = 'e700d1378fc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('danhmuc_van_bang_chuyen_mon',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_chuyen_mon', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('danhmuc_van_bang_chuyen_mon')
    # ### end Alembic commands ###
