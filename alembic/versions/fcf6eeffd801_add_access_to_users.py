"""add access to users

Revision ID: fcf6eeffd801
Revises: 8a9c1e7492c1
Create Date: 2026-04-16 18:41:48.991325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcf6eeffd801'
down_revision: Union[str, Sequence[str], None] = '8a9c1e7492c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "comments" not in inspector.get_table_names():
        op.create_table(
            "comments",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("film_id", sa.Integer(), nullable=False),
            sa.Column("comment_text", sa.String(), nullable=False),
            sa.ForeignKeyConstraint(["film_id"], ["films.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("id"),
        )

    access_enum = sa.Enum("USER", "ADMIN", name="accesslevel")
    user_columns = {column["name"]: column for column in inspector.get_columns("users")}

    if "access" not in user_columns:
        op.add_column("users", sa.Column("access", access_enum, nullable=True))

    op.execute("UPDATE users SET access = 'USER' WHERE access IS NULL")

    inspector = sa.inspect(bind)
    access_column = {column["name"]: column for column in inspector.get_columns("users")}.get("access")
    if access_column and access_column.get("nullable", True):
        with op.batch_alter_table("users") as batch_op:
            batch_op.alter_column("access", existing_type=access_enum, nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    user_columns = {column["name"] for column in inspector.get_columns("users")}
    if "access" in user_columns:
        with op.batch_alter_table("users") as batch_op:
            batch_op.drop_column("access")

    if "comments" in inspector.get_table_names():
        op.drop_table("comments")
