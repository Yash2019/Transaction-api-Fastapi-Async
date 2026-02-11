revision = "af69ec374da1"
down_revision = "e05aa79fe175"
branch_labels = None
depends_on = None



from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.add_column(
        "transactionlog",
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
    )
    op.alter_column(
        "transactionlog",
        "amount",
        existing_type=sa.Integer(),
        type_=sa.Numeric(),
        existing_nullable=False,
    )
    op.alter_column("transactionlog", "status", server_default=None)

def downgrade() -> None:
    op.alter_column(
        "transactionlog",
        "amount",
        existing_type=sa.Numeric(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.drop_column("transactionlog", "status")
