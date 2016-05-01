"""empty message

Revision ID: 54a34b49bac9
Revises: ef1dbd3fe501
Create Date: 2016-04-28 12:37:52.182625

"""

# revision identifiers, used by Alembic.
revision = '54a34b49bac9'
down_revision = 'ef1dbd3fe501'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    ### end Alembic commands ###