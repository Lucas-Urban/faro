"""empty message

Revision ID: 182833f9f212
Revises: 76d08083729a
Create Date: 2023-04-30 14:18:52.587188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '182833f9f212'
down_revision = '76d08083729a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('encontrar_pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data', sa.DateTime(), nullable=True))

    with op.batch_alter_table('encontrar_tutor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('encontrar_tutor', schema=None) as batch_op:
        batch_op.drop_column('data')

    with op.batch_alter_table('encontrar_pet', schema=None) as batch_op:
        batch_op.drop_column('data')

    # ### end Alembic commands ###
