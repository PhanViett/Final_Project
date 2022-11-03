"""update Table user 

Revision ID: c9c9d45f404a
Revises: 67f1310c3a67
Create Date: 2022-05-24 09:25:15.775924

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c9c9d45f404a'
down_revision = '67f1310c3a67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lk_thong_bao',
    sa.Column('thong_bao_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('thong_bao_user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['thong_bao_id'], ['thong_bao.id'], ),
    sa.ForeignKeyConstraint(['thong_bao_user_id'], ['thong_bao_user.id'], ),
    sa.PrimaryKeyConstraint('thong_bao_id', 'thong_bao_user_id')
    )
    op.add_column('thong_bao_user', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.drop_constraint('thong_bao_user_thong_bao_id_fkey', 'thong_bao_user', type_='foreignkey')
    op.drop_constraint('thong_bao_user_user_id_fkey', 'thong_bao_user', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('thong_bao_user_user_id_fkey', 'thong_bao_user', 'tai_khoan', ['user_id'], ['id'])
    op.create_foreign_key('thong_bao_user_thong_bao_id_fkey', 'thong_bao_user', 'thong_bao', ['thong_bao_id'], ['id'])
    op.alter_column('thong_bao_user', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('thong_bao_user', 'thong_bao_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('thong_bao_user', 'id')
    op.drop_table('lk_thong_bao')
    # ### end Alembic commands ###