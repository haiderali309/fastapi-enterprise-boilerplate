from typing import Optional
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from app.core.logging import logger


email_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
)


template_dir = Path(__file__).parent / "templates"

jinja_env = Environment( loader=FileSystemLoader(template_dir) )


async def send_mail(
    subject: str,
    message: str,
    recipient_list: list[str],
    template_name: Optional[str] = None,
    context: Optional[dict] = None
):
    html_message = None

    if template_name:
        template = jinja_env.get_template(template_name)
        html_message = template.render(**(context or {}))

    email = MessageSchema(
        subject=subject,
        recipients=recipient_list,
        body=html_message or message,
        subtype="html" if html_message else "plain"
    )

    await FastMail(email_config).send_message(email)
