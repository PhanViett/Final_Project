"""vietpv9

Revision ID: 33198ea571cf
Revises: 7725a3b41642
Create Date: 2022-08-24 10:32:45.779999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33198ea571cf'
down_revision = '7725a3b41642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('danhmuc_vi_tri_hanh_nghe', sa.Column('rut_gon', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('danhmuc_vi_tri_hanh_nghe', 'rut_gon')
    # ### end Alembic commands ###
