# src/services/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.exceptions import EmailException

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.emails_from_email = settings.EMAILS_FROM_EMAIL
        self.emails_from_name = settings.EMAILS_FROM_NAME

    def send_email(
        self,
        email_to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email"""
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            print(f"Email not sent - SMTP not configured")
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.emails_from_name} <{self.emails_from_email}>"
        msg["To"] = email_to

        # Attach text and HTML versions
        if text_content:
            part1 = MIMEText(text_content, "plain")
            msg.attach(part1)

        part2 = MIMEText(html_content, "html")
        msg.attach(part2)

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            raise EmailException(f"Failed to send email: {str(e)}")

    def send_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email to new user"""
        subject = f"Welcome to {settings.PROJECT_NAME}, {name}!"

        html_content = f"""
        <html>
            <body>
                <h1>Welcome to {settings.PROJECT_NAME}!</h1>
                <p>Hi {name},</p>
                <p>Thank you for joining our community. We're excited to have you on board!</p>
                <p>Start exploring our products and enjoy your shopping experience.</p>
                <br>
                <p>Best regards,<br>{settings.PROJECT_NAME} Team</p>
            </body>
        </html>
        """

        return self.send_email(email, subject, html_content)

    def send_password_reset_email(self, email: str, name: str, reset_url: str) -> bool:
        """Send password reset email"""
        subject = f"Password Reset Request - {settings.PROJECT_NAME}"

        html_content = f"""
        <html>
            <body>
                <h1>Reset Your Password</h1>
                <p>Hi {name},</p>
                <p>You requested to reset your password. Click the link below to set a new password:</p>
                <p><a href="{reset_url}">Reset Password</a></p>
                <p>This link will expire in {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <br>
                <p>Best regards,<br>{settings.PROJECT_NAME} Team</p>
            </body>
        </html>
        """

        return self.send_email(email, subject, html_content)