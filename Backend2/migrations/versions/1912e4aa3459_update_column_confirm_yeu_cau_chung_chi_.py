"""Update column confirm yeu_cau_chung_chi_hanh_nghe

Revision ID: 1912e4aa3459
Revises: bdfe82781ac3
Create Date: 2022-10-17 11:12:10.789336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1912e4aa3459'
down_revision = 'bdfe82781ac3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('confirm', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'confirm')
    # ### end Alembic commands ###
