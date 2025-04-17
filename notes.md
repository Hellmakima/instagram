**Web Security Concepts:**

* **CSRF (Cross-Site Request Forgery):**
    * Attack where a malicious site tricks a logged-in user into performing unwanted actions on a legitimate site *without their knowledge*.
    * Exploits the trust a website has in a user's browser.
    * Happens with *same-origin requests* (requests to the same website the user is on).
    * Example: Malicious link to transfer money on a banking site.
    * **Prevention:**
        * **CSRF Tokens:** Unique, random tokens in forms.
        * **SameSite Cookies:** Restrict cookies in cross-site requests.
        * **Referer Header Checking:** Verify the request origin.
        * **Custom Headers:** Require specific headers in requests.

* **CORS (Cross-Origin Resource Sharing):**
    * Security feature to control *cross-origin requests* (requests from a different domain, subdomain, or port).
    * Only affects HTTP requests (like AJAX or fetch).
    * **Does NOT prevent CSRF** because CSRF targets *same-origin requests*.

* **CSP (Content Security Policy):**
    * HTTP header or `<meta>` tag that allows developers to specify trusted sources for website content (scripts, styles, images, etc.).
    * Primarily protects against **XSS (Cross-Site Scripting)** and data injection attacks.
    * Works by the browser blocking content from unauthorized sources.
    * **Directives:** `default-src`, `script-src`, `style-src`, `img-src`, etc.
    * **Keywords:** `'self'`, `'unsafe-inline'`, `'unsafe-eval'`, `'none'`, `https://`.
    * **Benefits:** Prevents XSS, mitigates data injection, reduces attack surface, helps block mixed content.
    * **Reporting:** Can report violations using `report-uri` or `report-to`.
    * **Levels:** Basic, Strict, Nonce-based/Hash-based.
    * **Does NOT directly prevent CSRF** because CSRF exploits legitimate user actions within the same origin.
---

```python
# utils.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 20
REFRESH_EXPIRE_DAYS = 7

def create_refresh_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    data["type"] = "refresh"
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# routes.py
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer
from .utils import create_token, verify_token, create_refresh_token
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: LoginRequest, response: Response):
    # Replace this with your real user authentication logic
    access_token = create_token({"sub": data.username})
    refresh_token = create_refresh_token({"sub": data.username})
    csrf_token = str(uuid4())

    # Set access token as HttpOnly cookie with SameSite and Secure flags
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax" if more lenient behavior is needed
        max_age=60*20,      # Token expiration in seconds (20 minutes)
    )

    # Set refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax"
        max_age=60*60*24*7, # Longer expiration for refresh token (7 days)
    )

    # Set CSRF token as a regular cookie (accessible by JS)
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        secure=True,        # Only sent over HTTPS
        samesite="Strict",
        max_age=60*20,      # Same as access token for simplicity
    )

    return {"message": "Login successful"}

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh(data: RefreshRequest, response: Response):
    payload = verify_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Create a new access token
    new_access = create_token({"sub": payload["sub"]})
    new_csrf_token = str(uuid4())

    # Set the new access token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax" if more lenient behavior is needed
        max_age=60*20,      # Token expiration in seconds (20 minutes)
    )

    # Set the new CSRF token
    response.set_cookie(
        key="csrf_token",
        value=new_csrf_token,
        secure=True,        # Only sent over HTTPS
        samesite="Strict",
        max_age=60*20,      # Same as access token
    )

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }

@router.get("/me")
def me(request: Request, token: str = Depends(oauth2_scheme)):
    csrf_token = request.cookies.get("csrf_token")
    auth_header_csrf_token = request.headers.get("X-CSRF-Token")

    if not csrf_token or not auth_header_csrf_token or csrf_token != auth_header_csrf_token:
        raise HTTPException(status_code=403, detail="CSRF token mismatch")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": payload["sub"]}

# Optional: Logout route to delete cookies
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("csrf_token")
    return {"message": "Logged out successfully"}
```

**Explanation of Changes:**

**routes.py:**

1.  **CSRF Token Generation:**
    * On successful login (`/token`), a unique CSRF token is generated using `uuid4()`.
    * This token is set as a regular (non-`HttpOnly`) cookie named `csrf_token`. This makes it accessible by JavaScript on the client-side.

2.  **CSRF Token Setting on Refresh:**
    * When a new access token is issued during the refresh process (`/refresh`), a new CSRF token is also generated and set as a cookie.

3.  **CSRF Token Validation in `/me`:**
    * The `/me` endpoint now expects the CSRF token to be sent in a custom HTTP header named `X-CSRF-Token`.
    * It retrieves the `csrf_token` from the request cookies and the `X-CSRF-Token` from the request headers.
    * If either token is missing or they don't match, a `403 Forbidden` error is raised, indicating a potential CSRF attack.

4.  **CSRF Token Removal on Logout:**
    * The `/logout` endpoint now also deletes the `csrf_token` cookie.

**How to Use the CSRF Protection on the Client-Side:**

1.  **On Login:** After a successful login, your frontend JavaScript should read the `csrf_token` cookie.

2.  **Subsequent Requests:** For any subsequent requests to your backend that are not simple GET requests (e.g., POST, PUT, DELETE), your frontend JavaScript must:
    * Read the value of the `csrf_token` cookie.
    * Set this value as the value of the `X-CSRF-Token` HTTP header in the request.

**Important Considerations:**

* **Frontend Implementation:** This backend code sets up the CSRF protection, but you **must** implement the logic on your frontend to read the CSRF token from the cookie and include it in the `X-CSRF-Token` header for all state-changing requests.
* **Stateless Nature of JWT:** While this setup uses cookies for storage, the JWT itself remains stateless. The CSRF token acts as a stateful guard against malicious cross-site requests.
* **Simplicity:** This is a basic implementation. For more complex applications, you might consider using a dedicated CSRF protection library.

With these changes, your application now has a basic layer of CSRF protection when using cookie-based JWT authentication. Remember to implement the corresponding frontend logic!