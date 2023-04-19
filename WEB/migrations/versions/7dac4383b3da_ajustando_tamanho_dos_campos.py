"""ajustando tamanho dos campos

Revision ID: 7dac4383b3da
Revises: 6dd5c323ae88
Create Date: 2023-04-10 21:31:01.173483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dac4383b3da'
down_revision = '6dd5c323ae88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('encontrar_pet', schema=None) as batch_op:
        batch_op.alter_column('nome',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('local',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('tutor_nome',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('tutor_email',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('encontrar_pet', schema=None) as batch_op:
        batch_op.alter_column('tutor_email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('tutor_nome',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('local',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('nome',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=80),
               existing_nullable=True)

    # ### end Alembic commands ###
