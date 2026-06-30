from services.senders.base_sender import BaseSender
from services.senders.email_sender import EmailSender
from services.senders.teams_sender import TeamsSender


class SenderFactory:
    def __init__(
        self,
        email_sender: EmailSender,
            teams_sender: TeamsSender,
    ):
        self.senders: dict[str, BaseSender] = {
            "email": email_sender,
            "teams": teams_sender,
        }

    def get_sender(
        self,
        channel: str,
    ) -> BaseSender:
        sender = self.senders.get(channel)

        if sender is None:
            raise ValueError(f"Unsupported notification channel: {channel}")

        return sender