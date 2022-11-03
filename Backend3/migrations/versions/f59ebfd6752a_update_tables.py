"""update tables

Revision ID: f59ebfd6752a
Revises: 70e3414bbbf1
Create Date: 2022-10-22 16:34:12.842805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f59ebfd6752a'
down_revision = '70e3414bbbf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tai_khoan',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('tai_khoan', sa.String(), nullable=False),
    sa.Column('mat_khau', sa.String(), nullable=False),
    sa.Column('dien_thoai', sa.String(length=12), nullable=True),
    sa.Column('type', sa.SmallInteger(), nullable=True),
    sa.Column('last_login_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tai_khoan')
    )
    op.create_table('vai_tro',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ten', sa.String(length=80), nullable=False),
    sa.Column('ten_en', sa.String(), nullable=True),
    sa.Column('vai_tro', sa.Unicode(), nullable=True),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('delete_at', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ten')
    )
    op.drop_table('predicts')
    op.add_column('users', sa.Column('tai_khoan_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('users', sa.Column('vai_tro_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'users', 'vai_tro', ['vai_tro_id'], ['id'])
    op.create_foreign_key(None, 'users', 'tai_khoan', ['tai_khoan_id'], ['id'])
    op.drop_column('users', 'vai_tro')
    op.drop_column('users', 'tai_khoan')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tai_khoan', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('vai_tro', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'vai_tro_id')
    op.drop_column('users', 'tai_khoan_id')
    op.create_table('predicts',
    sa.Column('created_at', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('result', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='predicts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='predicts_pkey')
    )
    op.drop_table('vai_tro')
    op.drop_table('tai_khoan')
    # ### end Alembic commands ###