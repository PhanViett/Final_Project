"""Update data table

Revision ID: cea95701006d
Revises: 1d5a1ba4a00d
Create Date: 2022-07-05 08:30:01.681174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cea95701006d'
down_revision = '1d5a1ba4a00d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chung_chi_hanh_nghe', 'ngay_quyet_dinh')
    op.drop_column('chung_chi_hanh_nghe', 'ngay_hieu_luc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chung_chi_hanh_nghe', sa.Column('ngay_hieu_luc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('chung_chi_hanh_nghe', sa.Column('ngay_quyet_dinh', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
