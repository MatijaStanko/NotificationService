from sqlmodel import Session, select

from app.database import engine
from app.models import (
    ChannelConfig,
    NotificationTemplate,
    NotificationType,
)


def seed_database() -> None:
    with Session(engine) as session:
        notification_types = seed_notification_types(session)
        channel_configs = seed_channel_configs(session)

        seed_notification_templates(
            session=session,
            notification_types=notification_types,
            channel_configs=channel_configs,
        )


def seed_notification_types(session: Session) -> dict[str, NotificationType]:
    notification_type_codes = [
        "welcome_user",
        "password_reset",
        "payment_success",
        "appointment_reminder",
        "system_alert",
    ]

    notification_types = {}

    for code in notification_type_codes:
        notification_type = get_notification_type_by_code(
            session=session,
            code=code,
        )

        if notification_type is None:
            notification_type = NotificationType(
                code=code,
                is_active=True,
            )

            session.add(notification_type)
            session.commit()
            session.refresh(notification_type)

        notification_types[code] = notification_type

    return notification_types


def seed_channel_configs(session: Session) -> dict[str, ChannelConfig]:
    channel_config_data = [
        {
            "channel": "email",
            "provider": "smtp",
            "config": {
                "host": "smtp.example.com",
                "port": 587,
                "username": "notification@example.com",
                "from_email": "noreply@example.com",
                "use_tls": True,
            },
        },
        {
            "channel": "teams",
            "provider": "webhook",
            "config": {
                "webhook_url": "https://example.com/teams-webhook",
                "team_name": "Operations",
                "default_title": "System notification",
            },
        },
        {
            "channel": "viber",
            "provider": "viber_bot",
            "config": {
                "bot_name": "NotificationBot",
                "api_url": "https://example.com/viber-api",
                "sender_name": "Notify",
            },
        },
        {
            "channel": "whatsapp",
            "provider": "whatsapp_business",
            "config": {
                "business_account": "Notification Service",
                "api_url": "https://example.com/whatsapp-api",
                "sender_name": "Notify",
            },
        },
    ]

    channel_configs = {}

    for data in channel_config_data:
        channel_config = get_channel_config_by_channel(
            session=session,
            channel=data["channel"],
        )

        if channel_config is None:
            channel_config = ChannelConfig(
                channel=data["channel"],
                provider=data["provider"],
                config=data["config"],
                is_active=True,
            )

            session.add(channel_config)
            session.commit()
            session.refresh(channel_config)

        channel_configs[data["channel"]] = channel_config

    return channel_configs


def seed_notification_templates(
    session: Session,
    notification_types: dict[str, NotificationType],
    channel_configs: dict[str, ChannelConfig],
) -> None:
    template_data = [
        {
            "notification_type": "welcome_user",
            "channel": "email",
            "subject_template": "Dobrodošao, {{ first_name }}!",
            "body_template": (
                "Zdravo {{ first_name }}, dobrodošao u naš sistem. "
                "Aktiviraj nalog klikom na sledeći link: {{ activation_link }}."
            ),
            "required_variables": {
                "required": ["first_name", "activation_link"]
            },
        },
        {
            "notification_type": "welcome_user",
            "channel": "viber",
            "subject_template": None,
            "body_template": (
                "Zdravo {{ first_name }}! Dobrodošao. "
                "Aktiviraj nalog ovde: {{ activation_link }}"
            ),
            "required_variables": {
                "required": ["first_name", "activation_link"]
            },
        },
        {
            "notification_type": "welcome_user",
            "channel": "whatsapp",
            "subject_template": None,
            "body_template": (
                "👋 Zdravo {{ first_name }}, tvoj nalog je skoro spreman. "
                "Klikni za aktivaciju: {{ activation_link }}"
            ),
            "required_variables": {
                "required": ["first_name", "activation_link"]
            },
        },
        {
            "notification_type": "password_reset",
            "channel": "email",
            "subject_template": "Reset lozinke",
            "body_template": (
                "Zdravo {{ first_name }}, primili smo zahtev za reset lozinke. "
                "Link za reset je: {{ reset_link }}. "
                "Link važi {{ expiration_minutes }} minuta."
            ),
            "required_variables": {
                "required": ["first_name", "reset_link", "expiration_minutes"]
            },
        },
        {
            "notification_type": "password_reset",
            "channel": "viber",
            "subject_template": None,
            "body_template": (
                "{{ first_name }}, reset lozinke možeš izvršiti ovde: "
                "{{ reset_link }}. Link važi {{ expiration_minutes }} minuta."
            ),
            "required_variables": {
                "required": ["first_name", "reset_link", "expiration_minutes"]
            },
        },
        {
            "notification_type": "password_reset",
            "channel": "whatsapp",
            "subject_template": None,
            "body_template": (
                "🔐 {{ first_name }}, zatražen je reset lozinke. "
                "Link: {{ reset_link }}. Važi {{ expiration_minutes }} minuta."
            ),
            "required_variables": {
                "required": ["first_name", "reset_link", "expiration_minutes"]
            },
        },
        {
            "notification_type": "payment_success",
            "channel": "email",
            "subject_template": "Uplata je uspešno evidentirana",
            "body_template": (
                "Zdravo {{ first_name }}, vaša uplata od {{ amount }} {{ currency }} "
                "je uspešno evidentirana. ID transakcije: {{ transaction_id }}."
            ),
            "required_variables": {
                "required": ["first_name", "amount", "currency", "transaction_id"]
            },
        },
        {
            "notification_type": "payment_success",
            "channel": "viber",
            "subject_template": None,
            "body_template": (
                "Uplata uspešna ✅ Iznos: {{ amount }} {{ currency }}. "
                "Transakcija: {{ transaction_id }}."
            ),
            "required_variables": {
                "required": ["amount", "currency", "transaction_id"]
            },
        },
        {
            "notification_type": "payment_success",
            "channel": "whatsapp",
            "subject_template": None,
            "body_template": (
                "✅ {{ first_name }}, uplata od {{ amount }} {{ currency }} je uspešna. "
                "ID: {{ transaction_id }}"
            ),
            "required_variables": {
                "required": ["first_name", "amount", "currency", "transaction_id"]
            },
        },
        {
            "notification_type": "appointment_reminder",
            "channel": "email",
            "subject_template": "Podsetnik za zakazani termin",
            "body_template": (
                "Zdravo {{ first_name }}, podsećamo vas da imate zakazan termin "
                "{{ appointment_date }} u {{ appointment_time }}. "
                "Lokacija: {{ location }}."
            ),
            "required_variables": {
                "required": [
                    "first_name",
                    "appointment_date",
                    "appointment_time",
                    "location",
                ]
            },
        },
        {
            "notification_type": "appointment_reminder",
            "channel": "viber",
            "subject_template": None,
            "body_template": (
                "Podsetnik: termin je {{ appointment_date }} u {{ appointment_time }}. "
                "Lokacija: {{ location }}."
            ),
            "required_variables": {
                "required": ["appointment_date", "appointment_time", "location"]
            },
        },
        {
            "notification_type": "appointment_reminder",
            "channel": "whatsapp",
            "subject_template": None,
            "body_template": (
                "📅 {{ first_name }}, podsetnik za termin: "
                "{{ appointment_date }} u {{ appointment_time }}, {{ location }}."
            ),
            "required_variables": {
                "required": [
                    "first_name",
                    "appointment_date",
                    "appointment_time",
                    "location",
                ]
            },
        },
        {
            "notification_type": "system_alert",
            "channel": "email",
            "subject_template": "[{{ severity }}] Alert iz servisa {{ service_name }}",
            "body_template": (
                "Servis: {{ service_name }}\n"
                "Nivo: {{ severity }}\n"
                "Vreme: {{ timestamp }}\n"
                "Poruka: {{ message }}"
            ),
            "required_variables": {
                "required": ["service_name", "severity", "timestamp", "message"]
            },
        },
        {
            "notification_type": "system_alert",
            "channel": "teams",
            "subject_template": None,
            "body_template": (
                "🚨 **{{ severity }} alert**\n\n"
                "Service: {{ service_name }}\n"
                "Time: {{ timestamp }}\n"
                "Message: {{ message }}"
            ),
            "required_variables": {
                "required": ["service_name", "severity", "timestamp", "message"]
            },
        },
    ]

    for data in template_data:
        notification_type = notification_types[data["notification_type"]]
        channel_config = channel_configs[data["channel"]]

        existing_template = get_template_by_type_and_channel(
            session=session,
            notification_type_id=notification_type.id,
            channel_id=channel_config.id,
        )

        if existing_template is not None:
            continue

        notification_template = NotificationTemplate(
            notification_type_id=notification_type.id,
            channel_id=channel_config.id,
            subject_template=data["subject_template"],
            body_template=data["body_template"],
            required_variables=data["required_variables"],
            is_active=True,
        )

        session.add(notification_template)
        session.commit()


def get_notification_type_by_code(
    session: Session,
    code: str,
) -> NotificationType | None:
    statement = select(NotificationType).where(NotificationType.code == code)

    return session.exec(statement).first()


def get_channel_config_by_channel(
    session: Session,
    channel: str,
) -> ChannelConfig | None:
    statement = select(ChannelConfig).where(ChannelConfig.channel == channel)

    return session.exec(statement).first()


def get_template_by_type_and_channel(
    session: Session,
    notification_type_id: int,
    channel_id: int,
) -> NotificationTemplate | None:
    statement = (
        select(NotificationTemplate)
        .where(NotificationTemplate.notification_type_id == notification_type_id)
        .where(NotificationTemplate.channel_id == channel_id)
    )

    return session.exec(statement).first()