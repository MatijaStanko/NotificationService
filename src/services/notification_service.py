from abc import ABC, abstractmethod

from app.models import NotificationRequest
from app.schemas import NotificationCreate
from services.notification_type_service import NotificationTypeService
from services.notification_template_service import NotificationTemplateService
from services.channel_config_service import ChannelConfigService
from services.notification_request_service import NotificationRequestService

class INotificationSenderService(ABC):

    @abstractmethod
    def create_notification(self, data : NotificationCreate) -> NotificationRequest:
        pass


class NotificationService(INotificationSenderService):
    def __init__(
            self,
            notification_request_service: NotificationRequestService,
            notification_type_service: NotificationTypeService,
            channel_config_service: ChannelConfigService,
            notification_template_service: NotificationTemplateService,
    ):
        self.notification_request_service = notification_request_service
        self.notification_type_service = notification_type_service
        self.channel_config_service = channel_config_service
        self.notification_template_service = notification_template_service


    def create_notification(self, data : NotificationCreate) -> NotificationRequest:
        notification_type = self.notification_type_service.get_active_by_code(
            data.notification_type
        )

        channel_config = self.channel_config_service.get_active_by_channel(
            data.channel
        )

        template = self.notification_template_service.get_active_template(
            notification_type_id = notification_type.id,
            channel_id = channel_config.id
        )

        self.notification_template_service.validate_required_variables(
            required_variables = template.required_variables,
            template_data = data.template_data
        )

        rendered_subject = self.notification_template_service.render_subject(
            subject_template=template.subject_template,
            template_data=data.template_data
        )

        rendered_body = self.notification_template_service.render_body(
            body_template=template.body_template,
            template_data=data.template_data
        )

        notification_request = NotificationRequest(
            source_service = data.source_service,
            notification_type_id = notification_type.id,
            template_id = template.id,
            channel = data.channel,
            recipient = data.recipient,
            template_data = data.template_data,
            rendered_subject = rendered_subject,
            rendered_body = rendered_body,
            status = "pending"
        )

        return self.notification_request_service.create(notification_request)
