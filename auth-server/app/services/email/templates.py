# auth-server/app/services/email/templates.py

from app.core.config import settings

def get_verification_email_body(verification_link: str) -> str:
    """
    Generates the HTML body for the email verification message.
    """
    # A simple, secure HTML structure is best for transactional emails
    return f"""
<html>
  <body style="font-family: sans-serif; line-height: 1.6; margin:0; padding:0;">
    <h2>Verify Your Email Address</h2>
    <p>Thanks for signing up for Nmaa!</p>
    <p>Please click the link below to confirm your email address and activate your account. 
       This link will expire in {settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES} minutes.</p>
    <p>
      <a href="{verification_link}" 
         style="display:inline-block; padding:10px 20px; color:#fff; background-color:#0095f6; border-radius:5px; text-decoration:none; font-weight:bold;">
         Verify Account
      </a>
    </p>
    <p>If you did not sign up for this service, please ignore this email.</p>
    <div style="color:#888; font-size:12px; margin-top:20px;">
      <a href="https://nmaa.com" style="color:#888; text-decoration:none;">Nmaa.com</a> | 
      <a href="https://nmaa.com/contact" style="color:#888; text-decoration:none;">Contact</a>
    </div>
  </body>
</html>
"""