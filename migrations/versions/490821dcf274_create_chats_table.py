"""create_chats_table

Revision ID: 490821dcf274
Revises: 
Create Date: 2022-08-21 11:05:24.301495

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "490821dcf274"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chats",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("lang", sa.String(2), default="ru"),
        sa.Column("has_permissions", sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table("chats")
    pass
