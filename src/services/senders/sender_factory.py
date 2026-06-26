from services.senders.base_sender import BaseSender
from services.senders.email_sender import EmailSender


class SenderFactory:
    def __init__(
        self,
        email_sender: EmailSender,
    ):
        self.senders: dict[str, BaseSender] = {
            "email": email_sender,
        }

    def get_sender(
        self,
        channel: str,
    ) -> BaseSender:
        sender = self.senders.get(channel)

        if sender is None:
            raise ValueError(f"Unsupported notification channel: {channel}")

        return sender