"""empty message

Revision ID: 9a728cfbb15a
Revises: bc0e0b34afb4
Create Date: 2020-09-21 14:40:03.703130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a728cfbb15a'
down_revision = 'bc0e0b34afb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listing', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listing', 'status')
    # ### end Alembic commands ###
