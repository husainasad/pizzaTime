"""Initial migration

Revision ID: 41c686d65ff8
Revises: 
Create Date: 2024-11-13 23:44:44.491618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41c686d65ff8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pizzas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_pizzas_id'), 'pizzas', ['id'], unique=False)
    op.create_table('toppings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_toppings_id'), 'toppings', ['id'], unique=False)
    op.create_table('pizza_toppings',
    sa.Column('pizza_id', sa.Integer(), nullable=False),
    sa.Column('topping_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pizza_id'], ['pizzas.id'], ),
    sa.ForeignKeyConstraint(['topping_id'], ['toppings.id'], ),
    sa.PrimaryKeyConstraint('pizza_id', 'topping_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pizza_toppings')
    op.drop_index(op.f('ix_toppings_id'), table_name='toppings')
    op.drop_table('toppings')
    op.drop_index(op.f('ix_pizzas_id'), table_name='pizzas')
    op.drop_table('pizzas')
    # ### end Alembic commands ###
