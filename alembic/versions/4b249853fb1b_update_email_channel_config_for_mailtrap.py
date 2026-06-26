"""Update email channel config for Mailtrap

Revision ID: 4b249853fb1b
Revises: 0c50a272d1a4
Create Date: 2026-06-26 14:24:14.674098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b249853fb1b'
down_revision: Union[str, Sequence[str], None] = '0c50a272d1a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE channel_configs
        SET config = '{
               "host": "sandbox.smtp.mailtrap.io",
               "port": 587,
               "username_env": "MAILTRAP_USERNAME",
               "password_env": "MAILTRAP_PASSWORD",
               "from_email": "noreply@notification-service.local",
               "use_tls": true
           }'::jsonb,
           provider = 'smtp'
        WHERE channel = 'email';
        """
    )

def downgrade() -> None:
    op.execute(
        """
        UPDATE channel_configs
        SET config = '{
            "host": "smtp.example.com",
            "port": 587,
            "username": "notification@example.com",
            "from_email": "noreply@example.com",
            "use_tls": true
        }'::jsonb,
        provider = 'smtp'
        WHERE channel = 'email';
        """
    )
