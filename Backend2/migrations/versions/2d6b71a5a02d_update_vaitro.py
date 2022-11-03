"""update vaitro

Revision ID: 2d6b71a5a02d
Revises: 130ea3b4b1bc
Create Date: 2022-05-12 11:36:00.980213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2d6b71a5a02d'
down_revision = '130ea3b4b1bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lk_vai_tro_nhan_vien',
    sa.Column('vai_tro_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('nhan_vien_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['nhan_vien_id'], ['nhan_vien.id'], ),
    sa.ForeignKeyConstraint(['vai_tro_id'], ['vai_tro.id'], ),
    sa.PrimaryKeyConstraint('vai_tro_id', 'nhan_vien_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_vai_tro_nhan_vien')
    # ### end Alembic commands ###