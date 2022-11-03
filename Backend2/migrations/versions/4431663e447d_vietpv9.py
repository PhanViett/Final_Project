"""vietpv9

Revision ID: 4431663e447d
Revises: 33198ea571cf
Create Date: 2022-08-24 13:20:30.064918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4431663e447d'
down_revision = '33198ea571cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nhan_vien', sa.Column('so_nha_thuong_tru', sa.String(), nullable=True))
    op.add_column('nhan_vien', sa.Column('so_nha', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nhan_vien', 'so_nha')
    op.drop_column('nhan_vien', 'so_nha_thuong_tru')
    # ### end Alembic commands ###