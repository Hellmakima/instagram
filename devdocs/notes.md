# **Web Security Best Practices**

- Access tokens are stateless, meaning they do not require server-side session storage because all necessary information for authorization is encoded within the token itself.

### **A. CSRF (Cross-Site Request Forgery)**

some site makes a req from your browser and since you are logged in, it sends a token in the header.

1. **CSRF Tokens**:
   - Backend generates a unique token, stores it server-side, and sends it in a **non-HttpOnly cookie**.
   - Frontend stores it in its JS (so no one can access it).
   - Frontend includes the same token in a header (e.g., `X-CSRF-Token`).
   - Backend validates the cookie token against the header token.

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

2. **IP Tracking (Optional)**:
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

### **C. Overall**

- Use JWT (JSON Web Tokens) for access/refresh.
- Use random secure strings (128+ bits) for CSRF.
- Use OAuth 2.0 Authorization Code Flow with PKCE (recommended for SPAs).
- Include claims like sub, iat, exp in JWTs.
- Rotate refresh tokens on use (refresh token rotation).
  **Where to Store**
  | Token Type | Client Storage | Server Storage | DB Storage |
  | ------------- | ------------------------------- | ------------------------- | ---------------------- |
  | Access Token | **In-memory (JS variable)** | Never store | X |
  | Refresh Token | **HttpOnly, Secure cookie** | Optional (if blacklist) | (encrypted) |
  | CSRF Token | **DOM/form field or cookie** | Validate per session | Optional (per-session) |

---

**Reverse Proxy**

- detailed video on [reverse proxy](https://www.youtube.com/watch?v=m1MWjPKS5NM) (serve backend and frotend on same host)
- goes in over what it is
- DNS, ssl cert (https sites), etc
- docker linux setup

## OAuth2.0

- https://www.youtube.com/watch?v=8-0-8a0s-9w
- referance [postman blog](https://blog.postman.com/what-is-oauth-2-0/)
  - Uses
    - allow third party apps to use instagram without having to implement their own login system.
    - allows limited access to instagram data
    - no need to share user's password
  - agents
    - resource owner: This is the user that is granting third-party access to their data.
    - client: This is the third-party application that is requesting access to the resource owner,s data. When the resource owner grants access, the client gets an access token that can be used to request the resources within the granted scope.
    - authorization server: This is the server that is responsible for granting access to the client.
    - resource server: This is the server that is responsible for serving the client with the requested data.
  - flow
    - user logs in to instagram
    - instagram redirects user to client
    - client requests access token from authorization server
    - authorization server redirects client to instagram
    - instagram redirects client to resource server
    - resource server returns access token to client
    - client uses access token to access instagram data
- also [what-is-pkce](https://blog.postman.com/what-is-pkce/)

A ton of servers possible

1. **Auth Server** - Handles login, tokens, user creds
2. **Resource Server** - Protects and serves data
3. **Frontend Server** - Hosts your SPA or HTML views
4. **Gateway/Proxy Server** - Routes, rate-limits, logs; like a traffic cop
5. **File Server** - For static/media file uploads/downloads
6. **Cache Server** - Like Redis; holds session or temp data
7. **Database Server** - Holds your precious data
8. **Job/Worker Server** - For async/background tasks like emails
9. **Monitoring/Logging Server** - Watches everything
