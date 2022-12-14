"""Update data table

Revision ID: 394759a95d9c
Revises: 539e55bf7e0c
Create Date: 2022-07-05 10:49:58.622510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '394759a95d9c'
down_revision = '539e55bf7e0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nhan_vien', sa.Column('vai_tro_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'nhan_vien', 'vai_tro', ['vai_tro_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nhan_vien', type_='foreignkey')
    op.drop_column('nhan_vien', 'vai_tro_id')
    # ### end Alembic commands ###
