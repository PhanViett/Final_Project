"""udad

Revision ID: 28ad1d9ce350
Revises: 26cecdbfdd8e
Create Date: 2022-05-24 17:52:31.591828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '28ad1d9ce350'
down_revision = '26cecdbfdd8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lk_noi_tot_nghiep_chung_chi',
    sa.Column('noi_tot_nghiep_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('chung_chi_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['chung_chi_id'], ['danhmuc_chung_chi.id'], ),
    sa.ForeignKeyConstraint(['noi_tot_nghiep_id'], ['danhmuc_noi_tot_nghiep.id'], ),
    sa.PrimaryKeyConstraint('noi_tot_nghiep_id', 'chung_chi_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lk_noi_tot_nghiep_chung_chi')
    # ### end Alembic commands ###
