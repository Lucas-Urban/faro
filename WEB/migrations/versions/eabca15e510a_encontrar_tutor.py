"""encontrar_tutor

Revision ID: eabca15e510a
Revises: 7dac4383b3da
Create Date: 2023-04-25 20:25:30.657379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eabca15e510a'
down_revision = '7dac4383b3da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('encontrar_tutor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('local', sa.String(length=200), nullable=True),
    sa.Column('anjo_nome', sa.String(length=200), nullable=True),
    sa.Column('anjo_email', sa.String(length=100), nullable=True),
    sa.Column('anjo_telefone', sa.String(length=20), nullable=True),
    sa.Column('raca', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('encontrar_tutor_foto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encontrar_tutor_id', sa.Integer(), nullable=False),
    sa.Column('arquivo', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['encontrar_tutor_id'], ['encontrar_tutor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('encontrar_tutor_foto')
    op.drop_table('encontrar_tutor')
    # ### end Alembic commands ###
