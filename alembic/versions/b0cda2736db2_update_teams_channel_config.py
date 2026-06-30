"""Update teams channel config

Revision ID: b0cda2736db2
Revises: 4b249853fb1b
Create Date: 2026-06-30 10:41:17.749381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0cda2736db2'
down_revision: Union[str, Sequence[str], None] = '4b249853fb1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE channel_configs
        SET config = '{
                "webhook_url_env": "TEAMS_WEBHOOK_URL"
            }'::jsonb,
            provider = 'webhook',
            is_active = true
        WHERE channel = 'teams';
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE channel_configs
        SET config    = '{}',
            provider  = 'webhook',
            is_active = false
        WHERE channel = 'teams';
        """
    )
