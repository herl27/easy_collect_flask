"""empty message

Revision ID: a351e14e44a6
Revises: effb6759bb88
Create Date: 2018-05-04 16:31:54.498745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a351e14e44a6'
down_revision = 'effb6759bb88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('is_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teachers', 'is_delete')
    # ### end Alembic commands ###
