from app.models import NotificationRequest, ChannelConfig
from services.senders.base_sender import BaseSender

class EmailSender(BaseSender):
    def send(self, notification_request: NotificationRequest, channel_config: ChannelConfig) -> None:
        # For now we only simulate email sending.
        # Later this will use SMTP or external email provider.
        print("Sending email notification")
        print(f"Provider: {channel_config.provider}")
        print(f"Recipient: {notification_request.recipient}")
        print(f"Subject: {notification_request.rendered_subject}")
        print(f"Body: {notification_request.rendered_body}")