"""empty message

Revision ID: dc736d1268df
Revises: c8ca352dc35c
Create Date: 2023-06-19 21:12:49.844551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc736d1268df'
down_revision = 'c8ca352dc35c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('otp', sa.String(length=6), nullable=True))
    op.add_column('users', sa.Column('verifiedEmail', sa.String(length=5), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verifiedEmail')
    op.drop_column('users', 'otp')
    # ### end Alembic commands ###
