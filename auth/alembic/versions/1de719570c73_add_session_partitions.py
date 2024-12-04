"""add_session_partitions

Revision ID: 1de719570c73
Revises: a774591f5108
Create Date: 2024-12-04 21:24:17.857254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from datetime import datetime, timedelta, UTC


# revision identifiers, used by Alembic.
revision: str = '1de719570c73'
down_revision: Union[str, None] = 'a774591f5108'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def add_partitions() -> None:
    TABLE_NAME = "session"
    start_date = datetime.now(UTC).replace(tzinfo=None)

    for i in range(10):  # 5 лет, одна секция на полгода
        partition_start = start_date + timedelta(weeks=26 * i)
        partition_end = partition_start + timedelta(weeks=26)
        partition_name = f"{TABLE_NAME}_{partition_start.strftime('%Y%m')}"
        op.execute(
            f"CREATE TABLE IF NOT EXISTS {partition_name} "
            f"PARTITION OF {TABLE_NAME} "
            f"FOR VALUES FROM ('{partition_start}') TO ('{partition_end}')"
        )


def upgrade() -> None:
    add_partitions()


def downgrade() -> None:
    ...
