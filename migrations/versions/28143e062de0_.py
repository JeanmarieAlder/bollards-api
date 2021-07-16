"""empty message

Revision ID: 28143e062de0
Revises: 0df26df10c9c
Create Date: 2021-07-16 08:29:27.939270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28143e062de0'
down_revision = '0df26df10c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bollard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('b_number', sa.Integer(), nullable=False),
    sa.Column('b_letter', sa.String(length=3), nullable=True),
    sa.Column('b_name', sa.String(length=50), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('b_lat', sa.Numeric(precision=8, scale=5), nullable=False),
    sa.Column('b_lng', sa.Numeric(precision=8, scale=5), nullable=False),
    sa.Column('image_icon', sa.String(length=25), nullable=False),
    sa.Column('main_image', sa.String(length=25), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('b_number')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('profile_pic', sa.String(length=25), nullable=False),
    sa.Column('last_lat', sa.Numeric(precision=8, scale=5), nullable=False),
    sa.Column('last_lon', sa.Numeric(precision=8, scale=5), nullable=False),
    sa.Column('last_zoom', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.String(length=25), nullable=False),
    sa.Column('bollard_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bollard_id'], ['bollard.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bimage')
    op.drop_table('user')
    op.drop_table('bollard')
    # ### end Alembic commands ###
