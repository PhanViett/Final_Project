"""Update data table

Revision ID: b1b7f6dc6734
Revises: 3520dabaac35
Create Date: 2022-07-14 13:49:55.776643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1b7f6dc6734'
down_revision = '3520dabaac35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co_so_thuc_hanh', sa.Column('noi_dung_thuc_hanh_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'co_so_thuc_hanh', 'noi_dung_thuc_hanh', ['noi_dung_thuc_hanh_id'], ['id'])
    op.drop_column('co_so_thuc_hanh', 'noi_dung_thuc_hanh')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co_so_thuc_hanh', sa.Column('noi_dung_thuc_hanh', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'co_so_thuc_hanh', type_='foreignkey')
    op.drop_column('co_so_thuc_hanh', 'noi_dung_thuc_hanh_id')
    # ### end Alembic commands ###