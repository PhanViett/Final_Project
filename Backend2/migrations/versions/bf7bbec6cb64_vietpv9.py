"""vietpv9

Revision ID: bf7bbec6cb64
Revises: 7fe52eff6e30
Create Date: 2022-08-16 17:45:34.860700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf7bbec6cb64'
down_revision = '7fe52eff6e30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co_so_kinh_doanh', sa.Column('ngay_cap', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('co_so_kinh_doanh', 'ngay_cap')
    # ### end Alembic commands ###
