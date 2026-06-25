from services.senders.base_sender import BaseSender
from services.senders.email_sender import EmailSender

class SenderFactory(BaseSender):
    def __init__(self, email_sender: EmailSender):
        self.email_sender = email_sender

    def get_sender(self, channel: str) -> BaseSender:
        if channel == "email":
            return self.email_sender

        raise ValueError(f"Unsupported notification channel: {channel}")