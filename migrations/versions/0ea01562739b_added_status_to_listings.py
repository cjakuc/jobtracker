"""Added status to listings

Revision ID: 0ea01562739b
Revises: b1e6af92e715
Create Date: 2020-09-21 14:28:26.801628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea01562739b'
down_revision = 'b1e6af92e715'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listing', sa.Column('status', sa.Enum('no_response', 'rejected', 'offer', 'turned_down', 'accepted', name='applicationstatusenum'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listing', 'status')
    # ### end Alembic commands ###