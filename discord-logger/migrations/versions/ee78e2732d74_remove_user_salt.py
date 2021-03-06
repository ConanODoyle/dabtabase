"""remove user salt

Revision ID: ee78e2732d74
Revises: 966f78e4f9a1
Create Date: 2020-08-21 11:18:26.706170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee78e2732d74'
down_revision = '966f78e4f9a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user') as batch_op:
    	batch_op.drop_column('salt')
    # op.drop_column('user', 'salt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('salt', sa.VARCHAR(length=16), nullable=True))
    # ### end Alembic commands ###
