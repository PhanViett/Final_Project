"""update Table123 

Revision ID: 0e8d83556fc6
Revises: 5f7b52ad96ff
Create Date: 2022-05-24 08:18:30.680418

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e8d83556fc6'
down_revision = '5f7b52ad96ff'
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