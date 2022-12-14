"""update

Revision ID: 8fc55efa98f5
Revises: 1b6a66bc17b8
Create Date: 2022-08-05 11:02:32.393100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc55efa98f5'
down_revision = '1b6a66bc17b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loai_ma_chung_chi', sa.Column('mac_dinh', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loai_ma_chung_chi', 'mac_dinh')
    # ### end Alembic commands ###
