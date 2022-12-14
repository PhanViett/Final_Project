"""update Table thongbaouser  

Revision ID: 64bf3c1bb855
Revises: bcb3064dd9d6
Create Date: 2022-05-23 17:35:33.017678

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '64bf3c1bb855'
down_revision = 'bcb3064dd9d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lk_thong_bao',
    sa.Column('thong_bao', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('tai_khoan', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['tai_khoan'], ['tai_khoan.id'], ),
    sa.ForeignKeyConstraint(['thong_bao'], ['thong_bao.id'], ),
    sa.PrimaryKeyConstraint('thong_bao', 'tai_khoan')
    )
    op.add_column('thong_bao_user', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('thong_bao_user', 'id')
    op.drop_table('lk_thong_bao')
    # ### end Alembic commands ###
