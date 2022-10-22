"""Update data table gps

Revision ID: 93ef583e83cc
Revises: 8ec4c5290c04
Create Date: 2022-06-15 17:17:49.366722

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '93ef583e83cc'
down_revision = '8ec4c5290c04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loai_magps',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ma_gps', sa.String(), nullable=True),
    sa.Column('ten', sa.String(), nullable=True),
    sa.Column('ten_khong_dau', sa.String(), nullable=True),
    sa.Column('trang_thai', sa.Boolean(), nullable=True),
    sa.Column('so_da_cap', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loai_magps')
    # ### end Alembic commands ###
