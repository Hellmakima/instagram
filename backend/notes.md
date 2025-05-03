# **Web Security Best Practices**

_A comprehensive guide to securing JWT-based authentication and preventing common attacks_

---

## **1. Core Security Concepts**

### **A. CSRF (Cross-Site Request Forgery)**

**What it is**:

- An attack where a malicious site tricks a logged-in user into performing unwanted actions on a legitimate site.
- Exploits the browser's automatic cookie inclusion in same-origin requests.

**Prevention**:

1. **CSRF Tokens** (Synchronizer Token Pattern):

   - Backend generates a unique token, stores it server-side, and sends it in a **non-HttpOnly cookie**.
   - Frontend includes the same token in a header (e.g., `X-CSRF-Token`).
   - Backend validates the cookie token against the header token.

2. **Double Submit Cookie** (Stateless Alternative):

   - Token is stored in a cookie and also sent in a header/body.
   - Backend checks if both values match (no server-side storage).

3. **SameSite Cookies**:
   - Set `SameSite=Strict` or `Lax` to restrict cross-origin cookie sending.

**Example (Flask)**:

```python
from flask import request, make_response
import secrets

# Generate and set CSRF token
csrf_token = secrets.token_hex(32)
response.set_cookie("csrf_token", csrf_token, secure=True, samesite="Lax")

# Validate CSRF token
def validate_csrf():
    cookie_token = request.cookies.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")
    if not cookie_token or cookie_token != header_token:
        return {"error": "CSRF validation failed"}, 403
```

---

### **B. JWT Security**

**Best Practices**:

1. **Storage**:

   - Use **`HttpOnly`**, **`Secure`**, and **`SameSite=Strict` cookies** (not `localStorage`).
   - Avoid sensitive data in JWTs (use encryption/JWE if needed).

2. **Token Lifespan**:

   - Short-lived access tokens (15–30 mins).
   - Long-lived refresh tokens (stored server-side).

3. **Signing**:
   - Use asymmetric algorithms (`RS256`) over symmetric (`HS256`).

**Example (Flask-JWT-Extended)**:

```python
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  # Never hardcode!
```

---

### **C. CORS (Cross-Origin Resource Sharing)**

**What it is**:

- Controls cross-origin requests (different domain/port).
- **Does NOT prevent CSRF** (CSRF exploits same-origin requests).

**Implementation**:

- Configure allowed origins, methods, and headers in the backend.

**Example (Flask)**:

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend.com"]}})
```

---

### **D. CSP (Content Security Policy)**

**What it is**:

- Restricts sources for scripts, styles, etc., to prevent XSS.

**Example Header**:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'; style-src 'self' https://fonts.googleapis.com; img-src 'self' data:
```

---

## **2. Implementation Guide**

### **A. Backend (Flask) Setup**

1. **JWT Configuration**:

   - Use cookies with `HttpOnly`/`Secure`.
   - Implement refresh tokens with server-side storage.

2. **CSRF Protection**:

   - Generate tokens for state-changing requests (POST/PUT/DELETE).
   - Validate tokens in middleware.

3. **IP Tracking (Optional)**:
   - Hash/anonymize IPs for privacy compliance (GDPR).
   - Log temporarily (e.g., 30 days) for security monitoring.

**Example IP Anonymization**:

```python
import hashlib
def anonymize_ip(ip):
    return hashlib.sha256(ip.encode() + b"salt").hexdigest()
```

---

### **B. Frontend Integration**

1. **For JWT in Cookies**:

   - No token handling needed (cookies are auto-sent by the browser).
   - Include CSRF tokens in headers for non-GET requests.

2. **For JWT in `localStorage` (Not Recommended)**:
   - Manually attach tokens to requests via `Authorization: Bearer <token>`.

**Example (JavaScript)**:

```javascript
// Read CSRF token from cookie
function getCsrfToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_token="))
    ?.split("=")[1];
}

// Include in fetch requests
fetch("/api/data", {
  method: "POST",
  headers: {
    "X-CSRF-Token": getCsrfToken(),
    "Content-Type": "application/json",
  },
});
```

---

## **3. Common Pitfalls & Fixes**

| **Issue**               | **Solution**                         |
| ----------------------- | ------------------------------------ |
| `localStorage` for JWTs | Use `HttpOnly` cookies.              |
| Missing CSRF for APIs   | Validate tokens for POST/PUT/DELETE. |

---

## **4. Summary Checklist**

- [ ] Use `HttpOnly`/`Secure` cookies for JWTs.
- [ ] Implement CSRF tokens (Double Submit or Synchronizer).
- [ ] Set `SameSite=Lax` for cookies.
- [ ] Configure CORS for frontend-backend communication.
- [ ] Anonymize/hash IPs if tracking.
- [ ] Avoid `localStorage` for sensitive data.

**Key Principle**:

- **Backend handles security** (token validation, CSRF).
- **Frontend minimizes risks** (XSS prevention, token forwarding).

---

_Updated: [4/27/2025]_
_References: OWASP, RFC 8725, Flask-JWT-Extended docs_
