"""Update data table

Revision ID: cd3e53cfc2a9
Revises: 0cfe90b90f6a
Create Date: 2022-07-04 17:42:47.953597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3e53cfc2a9'
down_revision = '0cfe90b90f6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co_so_thuc_hanh', sa.Column('giay_chung_nhan', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('co_so_thuc_hanh', 'giay_chung_nhan')
    # ### end Alembic commands ###