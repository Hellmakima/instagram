# Lessons Learned

---

## **1. Web Security Best Practices**

### **Access Tokens**

**Access tokens are stateless**, meaning they do not require server-side session storage because all necessary information for authorization is encoded within the token itself.

### **CSRF (Cross-Site Request Forgery)**

A CSRF attack occurs when another site makes a request from your browser. Since you are logged in, your browser sends a valid session cookie or token in the header, executing an unwanted action.

**CSRF Tokens**:

- The backend generates a unique token, stores it server-side, and sends it in a **non-HttpOnly cookie**.
- The frontend stores this token in its JavaScript (so it cannot be accessed from outside).
- The frontend then includes the same token in a header (e.g., `X-CSRF-Token`) with every request.
- The backend validates the token from the cookie against the token in the request header.

### **JWT (JSON Web Token) Security**

A JWT contains data and its hash. You can only recreate the hash if you have the key, but the data itself is readable by anyone.

**Best Practices**:

- **Storage**: Use **`HttpOnly`**, **`Secure`**, and **`SameSite=Strict` cookies** for JWTs, not `localStorage`.
- Avoid storing sensitive data directly in JWTs. If sensitive data is necessary, use encryption (JWE).

### **CORS (Cross-Origin Resource Sharing)**

CORS is a browser-implemented security mechanism. When a web page (Origin A) tries to call an API (Origin B), the browser first confirms with Origin A to see if it is allowed to make requests to Origin B. At the backend of Origin B, you must add Origin A to the CORS policy to allow these requests.

### **CSP (Content Security Policy)**

CSP is a security header that restricts the sources for scripts, styles, etc., to prevent Cross-Site Scripting (XSS) attacks.

**Example Header**:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'; style-src 'self' https://fonts.googleapis.com; img-src 'self' data:
```

---

## **2. Implementation Guide**

### **Cross-Platform Authentication**

A **flawed approach** is using a single function that checks for a token in either a cookie or a header. This can make your mobile-facing API vulnerable to cookie-based CSRF attacks and creates an unclear API contract.

The **correct approach** is to maintain a single API version but with separate, explicit authentication flows:

1.  **For Web Browsers**: Use a dedicated endpoint (`/auth/login_web`) that returns an **`HttpOnly` cookie**. This prevents JavaScript from accessing the token, mitigating XSS attacks.
2.  **For Mobile/APIs**: Use a separate endpoint (`/auth/login_mobile`) that returns a **JWT in the JSON response body**. The client stores and sends this token in the `Authorization: Bearer` header. Use `OAuth2PasswordBearer` for these endpoints.

### **Backend (Flask/FastAPI) Setup**

- **CSRF Protection**: Generate tokens for state-changing requests (POST/PUT/DELETE) and validate them in middleware.
- **IP Tracking (Optional)**: Hash and anonymize IPs for privacy (e.g., GDPR) and log them temporarily (e.g., 30 days) for security monitoring.

<!-- end list -->

```python
import hashlib
def anonymize_ip(ip):
    return hashlib.sha256(ip.encode() + b"salt").hexdigest()
```

### **Frontend Setup**

- **For JWT in Cookies**: No token handling is needed as cookies are automatically sent by the browser. You only need to include CSRF tokens in headers for non-GET requests.

### **Overall Recommendations**

- Use JWT for access/refresh tokens.
- Use random, secure strings (128+ bits) for CSRF.
- Use **OAuth 2.0 Authorization Code Flow with PKCE** for Single Page Applications (SPAs).
- Include standard claims like `sub`, `iat`, and `exp` in JWTs.
- Implement refresh token rotation on use.

### **Token Storage Reference Table**

| Token Type        | Client Storage                    | Server Storage              | DB Storage             |
| :---------------- | :-------------------------------- | :-------------------------- | :--------------------- |
| **Access Token**  | **In-memory (JS variable)**       | Never store                 | X                      |
| **Refresh Token** | **`HttpOnly`**, **Secure cookie** | Optional (for blacklisting) | (encrypted)            |
| **CSRF Token**    | **DOM/form field or cookie**      | Validate per session        | Optional (per-session) |

---

## **3. Core Architectural Patterns**

### **Pydantic Models**

Pydantic models are a powerful tool for **data validation** and **settings management** in Python. They are primarily used for:

- **API Data Validation**: In FastAPI, they validate incoming request bodies and outgoing responses.
- **Configuration Management**: Validating application settings from environment variables or files.
- **Data Transformation**: Converting raw data from various sources into structured Python objects.
- **Internal Data Structures**: Creating clear, typed data structures within the application logic for improved readability and maintenance.

### **Database Layer (Repository Pattern)**

Having a separate layer between your FastAPI application and the database (a **Repository Pattern** or **Data Access Layer**) is a crucial best practice.

**Why it is crucial**:

- **Database Agnosticism**: It decouples your core application logic from the specific database technology.
- **Centralized Data Logic**: All database operations are consolidated in one place, making the codebase easier to understand and debug.
- **Improved Testability**: You can easily mock the data access layer for faster, more reliable unit tests without a real database connection.
- **Enforcement of Business Rules**: This layer can enforce data integrity and business rules.
- **Security**: It provides a controlled point of access to the database and can handle sanitization and parameterized queries to prevent attacks like SQL injection.
- **Performance Optimization**: It is a good place to implement caching and connection pooling.

### **API Versioning**

Versioning your API is a best practice that helps you:

- Handle multiple clients (mobile, CLI, etc.).
- Allow for a graceful rollout and deprecation of features.
- Make debugging easier by isolating issues to a specific version.
- Prevent breaking queued or long-lived requests during updates.
- Safely support rolling deploys.

---

## **4. Infrastructure & Broader Architecture**

### **Reverse Proxy**

A reverse proxy serves as a traffic cop, routing requests to the correct backend service. It can serve both the backend and frontend on the same host, and is also used for managing DNS, SSL certificates, and load balancing. A detailed video on this topic is available here: [reverse proxy](https://www.youtube.com/watch?v=m1MWjPKS5NM).

### **OAuth 2.0**

OAuth 2.0 is an authorization framework that allows third-party applications to obtain limited access to user accounts without sharing a password. For example, "Sign in with Google."

**Agents Involved**:

- **Resource Owner**: The user granting third-party access.
- **Client**: The third-party application requesting access.
- **Authorization Server**: The server granting access tokens to the client.
- **Resource Server**: The server providing the requested data.

Additional resources for OAuth 2.0 include a [Postman blog post](https://blog.postman.com/what-is-oauth-2-0/), an article on [PKCE](https://blog.postman.com/what-is-pkce/), and an article on [OAuth2 grant types](https://fusionauth.io/blog/understanding-oauth2-grant-types).

### **Multi-Server Architecture**

A modern, scalable application can be composed of many different types of servers to handle various services:

1.  **Auth Server**: Handles login, tokens, and user credentials.
2.  **Resource Server**: Protects and serves data.
3.  **Frontend Server**: Hosts your Single Page Application (SPA) or HTML views.
4.  **Gateway/Proxy Server**: Routes and rate-limits requests.
5.  **File Server**: Manages static and media file uploads/downloads.
6.  **Cache Server**: Like Redis, holds session or temporary data.
7.  **Database Server**: Stores all your precious data.
8.  **Job/Worker Server**: Manages asynchronous or background tasks like sending emails.
9.  **Monitoring/Logging Server**: Watches the health and performance of the entire system.

## 5. Nginx and Traefik

### **Tier 1: The First Line of Defense (Nginx/Traefik)**

Think of Nginx or Traefik as a bouncer at the door. Their job is to filter requests at a high level and prevent bad actors from even getting inside.

- **What they protect against**: General request floods, denial-of-service (DoS) attacks, and anonymous scraping.
- **How they do it**: They apply a coarse-grained rate limit, typically based on the source IP address. For example, you might configure Nginx to allow only 100 requests per second from a single IP on your public API, or a stricter 5 requests per minute on your login page.
- **Why it's important**: This layer is incredibly fast and efficient. It stops a significant amount of malicious traffic before it ever hits your FastAPI application, saving your app's resources for legitimate requests.

### **Tier 2: The Specific Business Logic (slowapi)**

`slowapi` and its Redis backend are for handling the nuanced logic that a proxy cannot. This is about protecting a specific user account, not just the API endpoint in general.

- **What they protect against**: Targeted brute-force attacks on a single user's account. This requires knowing the username and tracking its state.
- **How they do it**: Your FastAPI code, using `slowapi` and Redis, can perform a **stateful check**. It tracks the number of failed attempts for a specific username. This logic is much more granular than what a proxy can provide.
- **Why it's important**: This is how you implement the specific requirement you mentioned: "5 failed attempts and then suspend for 12 hours." This logic is tied to your business rules and requires a persistent store (Redis) to work across multiple application instances.

In a robust architecture, these two layers work in tandem to provide comprehensive security. The proxy handles the high-volume, low-effort attacks, while your application handles the specific, high-value logic for account protection.

---

## Python Decorators

**What are decorators?**

- A decorator is a function that wraps another function to extend or modify its behavior without changing its source code.

Common uses:

- Logging
- Authentication/permissions
- Caching/memoization
- Timing functions
- Input validation

Example:

```python
def deco(fn):
def wrapper(*a, \*\*kw):
print("Before")
res = fn(*a, \*\*kw)
print("After")
return res
return wrapper

@deco
def hello():
print("Hello")

hello()
```

Output:

```text
Before
Hello
After
```

---
