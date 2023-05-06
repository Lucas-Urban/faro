"""empty message

Revision ID: ed22c892d41a
Revises: 7bfd9b6e7eae
Create Date: 2023-05-05 21:52:31.742631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed22c892d41a'
down_revision = '7bfd9b6e7eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('encontrado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encontrar_pet_id', sa.Integer(), nullable=False),
    sa.Column('encontrar_tutor_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['encontrar_pet_id'], ['encontrar_pet.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['encontrar_tutor_id'], ['encontrar_tutor.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('encontrado')
    # ### end Alembic commands ###