"""Update data table

Revision ID: 3520dabaac35
Revises: bdc59d550c32
Create Date: 2022-07-14 13:47:15.573669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3520dabaac35'
down_revision = 'bdc59d550c32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'co_so_thuc_hanh', 'noi_dung_thuc_hanh', ['noi_dung_thuc_hanh'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'co_so_thuc_hanh', type_='foreignkey')
    # ### end Alembic commands ###
