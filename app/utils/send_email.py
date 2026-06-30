import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_email(to_email: str, subject: str, body: str) -> None:
    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = settings.mail_username
    message["To"] = to_email

    message.set_content(body)

    with smtplib.SMTP(settings.mail_server, settings.mail_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(
            settings.mail_username,
            settings.mail_password
        )

        smtp.send_message(message)