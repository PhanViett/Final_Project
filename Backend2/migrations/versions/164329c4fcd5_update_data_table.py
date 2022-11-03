"""Update data table

Revision ID: 164329c4fcd5
Revises: 13717c6d7574
Create Date: 2022-06-20 17:17:26.598152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '164329c4fcd5'
down_revision = '13717c6d7574'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chung_chi_hanh_nghe', sa.Column('ngay_cap', sa.String(), nullable=True))
    op.add_column('chung_chi_hanh_nghe', sa.Column('noi_cap', sa.String(), nullable=True))
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'noi_cap')
    op.drop_column('yeu_cau_chung_chi_hanh_nghe', 'ngay_cap')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('ngay_cap', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('yeu_cau_chung_chi_hanh_nghe', sa.Column('noi_cap', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('chung_chi_hanh_nghe', 'noi_cap')
    op.drop_column('chung_chi_hanh_nghe', 'ngay_cap')
    # ### end Alembic commands ###