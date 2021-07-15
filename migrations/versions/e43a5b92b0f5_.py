"""empty message

Revision ID: e43a5b92b0f5
Revises: f299033cf085
Create Date: 2021-07-15 11:31:58.679351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e43a5b92b0f5'
down_revision = 'f299033cf085'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_lat', sa.Numeric(precision=8, scale=5), nullable=False))
    op.add_column('user', sa.Column('last_lon', sa.Numeric(precision=8, scale=5), nullable=False))
    op.add_column('user', sa.Column('last_zoom', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_zoom')
    op.drop_column('user', 'last_lon')
    op.drop_column('user', 'last_lat')
    # ### end Alembic commands ###