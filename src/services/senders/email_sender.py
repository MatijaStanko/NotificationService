import os
import smtplib
from email.message import EmailMessage

from app.models import NotificationRequest, ChannelConfig
from services.senders.base_sender import BaseSender

class EmailSender(BaseSender):

    def send(
            self,
            notification_request: NotificationRequest,
            channel_config: ChannelConfig,
    ) -> None:
        config = channel_config.config

        host = config.get("host")
        port = config.get("port")
        username_env = config.get("username_env")
        password_env = config.get("password_env")
        from_email = config.get("from_email")
        use_tls = config.get("use_tls")

        if not host:
            raise ValueError("SMTP host is not configured")

        if not port:
            raise ValueError("SMTP port is not configured")

        if not username_env:
            raise ValueError("SMTP username_env is not configured")

        if not password_env:
            raise ValueError("SMTP password_env is not configured")

        if not from_email:
            raise ValueError("SMTP from_email is not configured")

        if not use_tls:
            raise ValueError("SMTP use_tls is not configured")

        username = os.getenv(username_env)
        password = os.getenv(password_env)

        if not username:
            raise ValueError("MAILTRAP_USERNAME is not configured in .env")

        if not password:
            raise ValueError("MAILTRAP_PASSWORD is not configured in .env")

        message = EmailMessage()
        message["From"] = from_email
        message["To"] = notification_request.recipient
        message["Subject"] = notification_request.rendered_subject or ""
        message.set_content(notification_request.rendered_body or "")

        with smtplib.SMTP(host, port) as smtp:
            if use_tls:
                smtp.starttls()

            smtp.login(username, password)
            smtp.send_message(message)