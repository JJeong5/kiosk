"""empty message

Revision ID: 838299aac7ef
Revises: d127c4968db7
Create Date: 2023-09-27 11:42:37.213271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '838299aac7ef'
down_revision = 'd127c4968db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('order_time',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('order_time',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)

    # ### end Alembic commands ###
