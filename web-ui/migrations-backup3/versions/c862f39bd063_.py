"""empty message

Revision ID: c862f39bd063
Revises: d77e922b33ca
Create Date: 2023-06-14 19:11:57.980781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c862f39bd063'
down_revision = 'd77e922b33ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('motor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('esp32pin', sa.String(length=2), nullable=False),
    sa.Column('pinFunction', sa.String(length=200), nullable=False),
    sa.Column('pinName', sa.String(length=200), nullable=False),
    sa.Column('switchState', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('esp32pin'),
    sa.UniqueConstraint('pinFunction'),
    sa.UniqueConstraint('pinName')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('motor')
    # ### end Alembic commands ###