# auth-server/app/services/email/verification.py

import logging
from app.core.config import settings
from app.core.security import create_email_verification_token, verify_token
from app.services.email.send import send_email
from app.services.email.templates import get_verification_email_body
from app.schemas.auth import TokenData, TokenSub
from app.repositories.interfaces import UserRepositoryInterface as UserRepository

flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("app_security")


async def send_verification_email(token_sub: TokenSub, email: str) -> bool:
    """
    Generates a verification token and sends the verification email to the user.
    """
    try:
        # 1. Create the token
        email_token = create_email_verification_token(token_sub)

        # 2. Generate the verification link
        # Assumes VERIFICATION_URL is configured as the base endpoint
        verification_link = f"{settings.EMAIL_VERIFICATION_URL}?token={email_token}"

        # 3. Get the email content
        subject = "Confirm Your Email Address for Instagram Clone"
        body = get_verification_email_body(verification_link=verification_link)

        # 4. Send the email
        sent = await send_email(
            to_email=email, subject=subject, body=body, subtype="html"
        )

        if sent:
            flow_logger.info(
                "Verification email successfully queued for user %s", token_sub.id
            )
        else:
            flow_logger.error(
                "Failed to send verification email for user %s", token_sub.id
            )
        return sent

    except Exception as e:
        flow_logger.error(
            "Critical error in sending verification email for user %s: %s", str(e)
        )
        return False


async def verify_email_token(token: str, user_repo: UserRepository) -> str | None:
    """
    Verifies the email verification token and marks the user as verified if valid.
    raise HTTPException if the token is invalid or expired.
    """
    flow_logger.info("Verifying email token")
    try:
        token_sub = verify_token(token, token_type="email_verification")
        if not token_sub:
            flow_logger.error("Token verification returned no data")
            return None

        user_id = token_sub.id
        # mark user as verified via repository
        updated = await user_repo.mark_as_verified(user_id)
        if updated:
            flow_logger.info("User %s email verified successfully.", user_id)
            return user_id
        else:
            flow_logger.warning(
                "User %s email verification did not update any record.", user_id
            )
            return None
    except Exception as e:
        flow_logger.error("Error verifying email token: %s", str(e))
        raise
