"""create users table and course creator relation

Revision ID: 20260926_1415
Revises: 20260926_1403
Create Date: 2026-09-26 14:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260926_1415"
down_revision: Union[str, None] = "20260926_1403"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), server_default="STUDENT", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("role IN ('STUDENT', 'ADMIN')", name="ck_users_role"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # Nullable keeps this migration safe for databases that already contain
    # courses created before User/authentication existed. New admin APIs can
    # require creator_id after existing rows are backfilled.
    op.add_column(
        "courses",
        sa.Column("creator_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index("ix_courses_creator_id", "courses", ["creator_id"], unique=False)
    op.create_foreign_key(
        "fk_courses_creator_id_users",
        "courses",
        "users",
        ["creator_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_courses_creator_id_users", "courses", type_="foreignkey")
    op.drop_index("ix_courses_creator_id", table_name="courses")
    op.drop_column("courses", "creator_id")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
