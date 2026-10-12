"""Initial migration creating all tables:
- users
- loans
- collateral
- repayments
- borrower_payback_status
- payback_analysis_tally
- transactions
- notifications

Revision ID: 0001_initial
Revises: None
Create Date: 2026-10-12 18:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. loans table
    op.create_table(
        'loans',
        sa.Column('loan_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('borrower_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('interest_rate', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('term_months', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['borrower_id'], ['users.user_id']),
        sa.PrimaryKeyConstraint('loan_id'),
    )
    op.create_index(op.f('ix_loans_loan_id'), 'loans', ['loan_id'], unique=False)

    # 3. collateral table
    op.create_table(
        'collateral',
        sa.Column('collateral_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('borrower_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(length=100), nullable=True),
        sa.Column('value', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('verification_status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['borrower_id'], ['users.user_id']),
        sa.PrimaryKeyConstraint('collateral_id'),
    )
    op.create_index(op.f('ix_collateral_collateral_id'), 'collateral', ['collateral_id'], unique=False)

    # 4. borrower_payback_status table
    op.create_table(
        'borrower_payback_status',
        sa.Column('status_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('borrower_id', sa.Integer(), nullable=True),
        sa.Column('total_loans', sa.Integer(), nullable=True),
        sa.Column('total_repaid', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('delinquency_rate', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('risk_grade', sa.String(length=10), nullable=True),
        sa.ForeignKeyConstraint(['borrower_id'], ['users.user_id']),
        sa.PrimaryKeyConstraint('status_id'),
    )
    op.create_index(
        op.f('ix_borrower_payback_status_status_id'),
        'borrower_payback_status',
        ['status_id'],
        unique=False,
    )

    # 5. payback_analysis_tally table
    op.create_table(
        'payback_analysis_tally',
        sa.Column('tally_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('total_loans', sa.Integer(), nullable=True),
        sa.Column('avg_pd', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('avg_ltv', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('avg_repayment_time', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('tally_id'),
    )
    op.create_index(
        op.f('ix_payback_analysis_tally_tally_id'),
        'payback_analysis_tally',
        ['tally_id'],
        unique=False,
    )

    # 6. repayments table
    op.create_table(
        'repayments',
        sa.Column('repayment_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('loan_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['loan_id'], ['loans.loan_id']),
        sa.PrimaryKeyConstraint('repayment_id'),
    )
    op.create_index(op.f('ix_repayments_repayment_id'), 'repayments', ['repayment_id'], unique=False)

    # 7. transactions table
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('loan_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['loan_id'], ['loans.loan_id']),
        sa.PrimaryKeyConstraint('transaction_id'),
    )
    op.create_index(op.f('ix_transactions_transaction_id'), 'transactions', ['transaction_id'], unique=False)

    # 8. notifications table
    op.create_table(
        'notifications',
        sa.Column('notification_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.Enum('EMAIL', 'SMS', 'IN_APP', name='notification_channel'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), server_default=sa.text('0'), nullable=True),
        sa.Column(
            'priority',
            sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='notification_priority'),
            server_default='LOW',
            nullable=True,
        ),
        sa.Column('related_loan_id', sa.Integer(), nullable=True),
        sa.Column('related_txn_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['related_loan_id'], ['loans.loan_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['related_txn_id'], ['transactions.transaction_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('notification_id'),
    )
    op.create_index(op.f('ix_notifications_notification_id'), 'notifications', ['notification_id'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)
    op.create_index(op.f('ix_notifications_priority'), 'notifications', ['priority'], unique=False)
    op.create_index(op.f('ix_notifications_created_at'), 'notifications', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop in reverse dependency order
    op.drop_index(op.f('ix_notifications_created_at'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_priority'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_is_read'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_notification_id'), table_name='notifications')
    op.drop_table('notifications')

    op.drop_index(op.f('ix_transactions_transaction_id'), table_name='transactions')
    op.drop_table('transactions')

    op.drop_index(op.f('ix_repayments_repayment_id'), table_name='repayments')
    op.drop_table('repayments')

    op.drop_index(op.f('ix_payback_analysis_tally_tally_id'), table_name='payback_analysis_tally')
    op.drop_table('payback_analysis_tally')

    op.drop_index(op.f('ix_borrower_payback_status_status_id'), table_name='borrower_payback_status')
    op.drop_table('borrower_payback_status')

    op.drop_index(op.f('ix_collateral_collateral_id'), table_name='collateral')
    op.drop_table('collateral')

    op.drop_index(op.f('ix_loans_loan_id'), table_name='loans')
    op.drop_table('loans')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
