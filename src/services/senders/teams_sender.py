import os
import requests

from app.models import ChannelConfig, NotificationRequest
from services.senders.base_sender import BaseSender

class TeamsSender(BaseSender):
    def send(
            self,
            notification_request: NotificationRequest,
            channel_config: ChannelConfig,
    ) -> None:
        config = channel_config.config

        webhook_url_env = config.get("webhook_url_env")

        if not webhook_url_env:
            raise ValueError("Teams webhook_url_env is not configured")

        webhook_url = os.getenv(webhook_url_env)

        if not webhook_url:
            raise ValueError(f"{webhook_url_env} is not configured in environment variables")

        payload = self._build_payload(notification_request)

        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise ValueError(
                f"Teams webhook request failed with status {response.status_code}: {response.text}"
            )

    def _build_payload(
            self,
            notification_request: NotificationRequest,
    ) -> dict:
        title = notification_request.rendered_subject or "Notification"
        text = notification_request.rendered_body or ""

        return {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": title,
                    "weight": "Bolder",
                    "size": "Medium",
                    "wrap": True,
                },
                {
                    "type": "TextBlock",
                    "text": text,
                    "wrap": True,
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {
                            "title": "Source service",
                            "value": notification_request.source_service or "-",
                        },
                        {
                            "title": "Channel",
                            "value": notification_request.channel,
                        },
                        {
                            "title": "Recipient",
                            "value": notification_request.recipient,
                        },
                    ],
                },
            ],
        }