"""Update data table

Revision ID: 1d5a1ba4a00d
Revises: cd3e53cfc2a9
Create Date: 2022-07-05 08:26:38.219253

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d5a1ba4a00d'
down_revision = 'cd3e53cfc2a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chung_chi_hanh_nghe', 'thoi_gian_yeu_cau_lien_ket')
    op.drop_column('chung_chi_hanh_nghe', 'thoi_gian_tu_choi_lien_ket')
    op.drop_column('chung_chi_hanh_nghe', 'thoi_gian_duyet_lien_ket')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chung_chi_hanh_nghe', sa.Column('thoi_gian_duyet_lien_ket', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('chung_chi_hanh_nghe', sa.Column('thoi_gian_tu_choi_lien_ket', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('chung_chi_hanh_nghe', sa.Column('thoi_gian_yeu_cau_lien_ket', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
