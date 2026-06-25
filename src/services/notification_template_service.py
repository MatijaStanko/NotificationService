from abc import ABC, abstractmethod

from app.models import NotificationTemplate
from repositories.notification_template_repository import NotificationTemplateRepository

class INotificationTemplateService(ABC):
    @abstractmethod
    def get_active_template(self, notification_type_id : int, channel_id : int) -> NotificationTemplate:
        pass

    @abstractmethod
    def validate_required_variables(self, required_variables: dict, template_data: dict) -> None:
        pass

    @abstractmethod
    def render_subject(self, subject_template : str | None, template_data : dict) -> None:
        pass

    @abstractmethod
    def render_body(self, body_template : str | None, template_data : dict) -> None:
        pass

    @abstractmethod
    def render_template(self, template : str | None, template_data : dict) -> str | None:
        pass


class NotificationTemplateService(INotificationTemplateService):
    def __init__(self, notification_template_repository: NotificationTemplateRepository):
        self.notification_template_repository = notification_template_repository

    def get_active_template(
            self,
            notification_type_id : int,
            channel_id : int
    ) -> NotificationTemplate:
        template = self.notification_template_repository.get_by_type_and_channel(
            notification_type_id,
            channel_id
        )

        if template is None:
            raise ValueError("Template does not exist for this notification type and channel")

        if not template.is_active:
            raise ValueError("Template is inactive")

        return template


    def validate_required_variables(
            self,
            required_variables : dict,
            template_data: dict
    ) -> None:
        required_variables_list = required_variables.get("required", [])

        missing_variables = []

        for variable in required_variables_list:
            if variable not in template_data:
                missing_variables.append(variable)

        if missing_variables:
            raise ValueError(f"Missing required variables: {missing_variables}")


    def render_subject(
            self,
            subject_template : str | None,
            template_data : dict
    ) -> str | None:
        return self.render_template(
            template = subject_template,
            template_data = template_data
        )

    def render_body(
            self,
            body_template : str | None,
            template_data : dict
    ) -> str:
        rendered_body = self.render_template(
            template = body_template,
            template_data = template_data
        )

        if rendered_body is None:
            raise ValueError("Body template cannot be empty")

        return rendered_body


    def render_template(
            self,
            template : str | None,
            template_data : dict
    ) -> str | None:

        if template is None:
            return None

        rendered_template = template

        for key, value in template_data.items():
            rendered_template = rendered_template.replace(
                "{{" + key + "}}",
                str(value)
            )
            rendered_template = rendered_template.replace(
                "{{ " + key + " }}",
                str(value)
            )

        return rendered_template
