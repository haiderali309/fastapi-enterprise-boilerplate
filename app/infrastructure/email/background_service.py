from app.infrastructure.email.service import send_mail
from app.core.logging import logger


async def send_mail_background(**kwargs):
    try:
        await send_mail(**kwargs)

        logger.info("Email sent successfully")

    except Exception:
        logger.exception("Background email failed")