from fastapi_csrf_protect import CsrfProtect
from pydantic_settings import BaseSettings
from fastapi_csrf_protect.exceptions import CsrfProtectError

# Config class
class CsrfSettings(BaseSettings):
    secret_key: str = "asecrettoeverybody"
    cookie_samesite: str = "lax"

# Load config
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# Main test
def main():
    csrf = CsrfProtect()
    csrf_token, signed_token = csrf.get_csrf_token()

    print("CSRF Token (client):", csrf_token)
    print("Signed Token (server):", signed_token)

    try:
        # Simulate validation: client sends csrf_token, server reads signed_token
        csrf.validate_csrf(csrf_token)
        print("CSRF Token is valid.")
    except CsrfProtectError as e:
        print("CSRF validation failed:", e.message)

if __name__ == "__main__":
    main()
