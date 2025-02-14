import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
import pytz
from botocore.exceptions import ClientError
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authentication import create_access_token, decode_jwt
from app.core.config import auth_settings, email_settings
from app.data_access.user_crud import get_user_by_username, save_user_verify
from app.models.email_verification import EmailVerificationRequest
from app.utils import AuthenticationError, get_logger

logger = get_logger(__name__)


class EmailService:
    def __init__(
        self, ses_client: boto3.client, source_email: str, source_domain
    ) -> None:
        self.ses_client = ses_client
        self.source_email = source_email
        self.source_domain = source_domain

    async def send_email(
        self,
        db_session,
        html_template: Template,
        email_verification_request: EmailVerificationRequest,
    ):
        evr = email_verification_request
        email = evr.email
        token = evr.token
        logger.info(f"username: {evr.email}")
        user = await get_user_by_username(db_session, evr.email)
        if user:
            if not token:
                token = create_access_token(
                    data={"sub": email, "scope": "email"},
                    expires_delta=auth_settings.signup_token_expire_minutes,
                )
            logger.info(f"Sending email from {self.source_email} to {email}")
            subject = "Confirm UrFit.io Account"
            verification_link = f"{self.source_domain}/email-verification/verify?email={email}&token={evr.token}"
            text_body = f"""
            Welcome to urfit.io.

            Thanks for joining our community!
            Please verify your email to activate your account:
                {verification_link}

            Have questions? Reply to this email—we’d love to help!

            © 2025 urfit.io. All rights reserved.

            Follow us on:
            Instagram: https://instagram.com/urfit.io
            Facebook: https://facebook.com/urfit.io
            Twitter: https://twitter.com/urfit_io
            """
            html_body = html_template.render(
                email=email, verification_link=verification_link
            )

            await self._send_email(email, subject, text_body, html_body)

            logger.info("Email sent")
            return True
        logger.info("no email sent")
        # raise AuthenticationError

    async def verify_email(self, db_session: AsyncSession, email: str, token: str):
        try:
            token: dict = decode_jwt(token)
            # if the token is valid, mark user as valid and return true
            # if the token is invalid then raise an exception
            user = await save_user_verify(
                db_session,
                username=email,
                is_verified=True,
                updated_date=datetime.now(pytz.timezone("America/Los_Angeles")),
            )
            return user
        except ValueError:
            raise

    async def resend_email(self, db_session: AsyncSession, email: str):
        user = await get_user_by_username(db_session, email)
        if user:
            access_token = create_access_token(
                data={"sub": email, "scope": "email"},
                expires_delta=auth_settings.signup_token_expire_minutes,
            )
            await self._send_email(
                self.source_email,
            )

    async def send_password_reset_email(
        self, db_session, template: Template, email: dict
    ):
        email = email.get("email")
        user = await get_user_by_username(db_session, email)
        logger.info(f"user {user}")
        if user.username:
            token = create_access_token(
                data={"sub": email, "scope": "email"},
                expires_delta=auth_settings.signup_token_expire_minutes,
            )

            reset_link = (
                f"{self.source_domain}/password-reset?email={email}&token={token}"
            )
            html_body = template.render(reset_link=reset_link)
            text_body = f"""
                Hello {email}
                Reset your password from the link below:
                {reset_link}
                """
            await self._send_email(
                email, "UrFit.io Password reset", text_body, html_body
            )

    async def _send_email(
        self, email: str, subject: str, text_body: str, html_body: str
    ):
        msg = MIMEMultipart("alternative")
        msg["From"] = f"UrFit.io <{self.source_email}>"
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        try:
            with smtplib.SMTP(
                email_settings.SMTP_SERVER, email_settings.SMTP_PORT
            ) as server:
                server.starttls()
                server.login(email_settings.SMTP_USERNAME, email_settings.SMTP_PASSWORD)
                server.sendmail(self.source_email, email, msg.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


import boto3

ses = boto3.client("ses", region_name="us-west-2")  # Adjust region if needed
from jinja2 import Environment, FileSystemLoader

template_loader = FileSystemLoader(
    searchpath="app/templates"
)  # Directory where your template is located
template_env = Environment(loader=template_loader)
template = template_env.get_template("/email/email_template.html")
print(template)
# template = {
#     'TemplateName': 'MyTemplate',
#     'SubjectPart': 'Welcome to UrFit.io',
#     'TextPart': """
#             Welcome to urfit.io.

#             Hi {{ email }},

#             Thanks for joining our community!
#             Please verify your email to activate your account:
#                 {{ verification_link }}

#             Have questions? Reply to this email—we’d love to help!

#             © 2025 urfit.io. All rights reserved.

#             Follow us on:
#             Instagram: https://instagram.com/urfit.io
#             Facebook: https://facebook.com/urfit.io
#             Twitter: https://twitter.com/urfit_io
#             """,
#     'HtmlPart': '<html><body><h1>Hello {{name}},</h1><p>Your account has been updated.</p></body></html>'
# }

# try:
#     response = ses.create_template(Template=template)
#     print("Template created successfully:", response)
# except Exception as e:
#     print("Error creating template:", e)
