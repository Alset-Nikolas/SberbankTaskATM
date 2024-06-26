"""Init Tables

Revision ID: 77241a0f952c
Revises: 
Create Date: 2024-05-19 12:02:05.269308

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '77241a0f952c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'currencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'bills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('currency_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('currency_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.VARCHAR(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('modified_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'bank_bills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'transaction_bills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('modified_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_bills')
    op.drop_table('bank_bills')
    op.drop_table('transactions')
    op.drop_table('bills')
    op.drop_table('currencies')
    # ### end Alembic commands ###
