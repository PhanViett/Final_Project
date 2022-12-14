"""Update data table

Revision ID: 05dc96b27f8b
Revises: 06bdacab4599
Create Date: 2022-07-20 14:11:48.804994

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '05dc96b27f8b'
down_revision = '06bdacab4599'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('lich_su_chung_chi_vai_tro_id_fkey', 'lich_su_chung_chi', type_='foreignkey')
    op.drop_column('lich_su_chung_chi', 'vai_tro_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lich_su_chung_chi', sa.Column('vai_tro_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('lich_su_chung_chi_vai_tro_id_fkey', 'lich_su_chung_chi', 'vai_tro', ['vai_tro_id'], ['id'])
    # ### end Alembic commands ###
