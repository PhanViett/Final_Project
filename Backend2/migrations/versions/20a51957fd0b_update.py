"""update

Revision ID: 20a51957fd0b
Revises: 166ff77328a5
Create Date: 2022-06-13 17:01:38.408031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a51957fd0b'
down_revision = '166ff77328a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('trang_thai_het_han', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'trang_thai_het_han')
    # ### end Alembic commands ###
