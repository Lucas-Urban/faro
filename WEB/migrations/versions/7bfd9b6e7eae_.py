"""empty message

Revision ID: 7bfd9b6e7eae
Revises: 182833f9f212
Create Date: 2023-05-01 15:11:27.873280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bfd9b6e7eae'
down_revision = '182833f9f212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nao_apresentar',
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
    op.drop_table('nao_apresentar')
    # ### end Alembic commands ###
