import logging
from typing import Optional
from app.core.config import settings
import smtplib
from email.message import EmailMessage

flow_logger = logging.getLogger("app_flow")


async def send_email(
    to_email: str, subject: str, body: str, subtype: str = "plain"
) -> bool:
    """
    Sends an email using SMTP in the style of the reference example.
    """
    try:
        msg = EmailMessage()
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body, subtype=subtype)

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(settings.SMTP_USER, settings.SMTP_APP_PASS)
            s.send_message(msg)

        flow_logger.info("Email sent via SMTP to %s", to_email)
        return True

    except Exception as e:
        flow_logger.error("Failed to send email to %s: %s", to_email, str(e))
        return False
