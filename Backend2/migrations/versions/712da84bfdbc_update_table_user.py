"""update Table user 

Revision ID: 712da84bfdbc
Revises: 14e239d347dd
Create Date: 2022-05-24 10:10:45.134338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '712da84bfdbc'
down_revision = '14e239d347dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('thong_bao_user', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.drop_constraint('thong_bao_user_user_id_fkey', 'thong_bao_user', type_='foreignkey')
    op.create_foreign_key(None, 'thong_bao_user', 'nhan_vien', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'thong_bao_user', type_='foreignkey')
    op.create_foreign_key('thong_bao_user_user_id_fkey', 'thong_bao_user', 'tai_khoan', ['user_id'], ['id'])
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('thong_bao_user', 'id')
    # ### end Alembic commands ###
