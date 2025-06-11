# **Web Security Best Practices**
- Access tokens are stateless, meaning they do not require server-side session storage because all necessary information for authorization is encoded within the token itself.

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

---

### **B. JWT Security**

**Best Practices**:
jWT has data and its hash. u can only recreate the hash if u have key. data is readable by anyone

1. **Storage**:

   - Use **`HttpOnly`**, **`Secure`**, and **`SameSite=Strict` cookies** (not `localStorage`).
   - Avoid sensitive data in JWTs (use encryption/JWE if needed).

---

### **C. CORS (Cross-Origin Resource Sharing)**

**What it is**:

- When one page (A) on browser tries to call some other API (B), the browser first confirms with the A to see if B is allowed to make requests. This is completely implemented by browser.
- At backend of B we need to add A in CORS policy to allow it to make requests.

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

1. **CSRF Protection**:

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

### **B. Frontend**

1. **For JWT in Cookies**:

   - No token handling needed (cookies are auto-sent by the browser).
   - Include CSRF tokens in headers for non-GET requests.

---

**Key Principle**:

- **Backend handles security** (token validation, CSRF).
- **Frontend minimizes risks** (XSS prevention, token forwarding).

---

**Reverse Proxy**
- detailed video on [reverse proxy](https://www.youtube.com/watch?v=m1MWjPKS5NM) (serve backend and frotend on same host)
- goes in over what it is
- DNS, ssl cert (https sites), etc
- docker linux setup
