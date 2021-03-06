"""Turned off index on listing description

Revision ID: b1e6af92e715
Revises: dc92d98cc319
Create Date: 2020-09-15 00:56:43.912371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e6af92e715'
down_revision = 'dc92d98cc319'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_listing_description', table_name='listing')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_listing_description', 'listing', ['description'], unique=False)
    # ### end Alembic commands ###
