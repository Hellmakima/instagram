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

## Testing FastAPI + Motor + MongoDB with pytest

We'll focus mainly on **unit testing** with `pytest`.

### pytest

### from a [tutorial](https://www.youtube.com/watch?v=mzlH8lp4ISA) and beloved [ChatGPT](https://chatgpt.com/?temporary-chat=true)
Rule of thumb: **don't test everything, test what can break.**


### General guidelines

- **Fixtures (`conftest.py`)**:

  - Shared setup/teardown helpers.
  - Declared once, available across all tests in that directory tree.
  - Great for DB setup, app clients, mock configs.

- **Parametrization** → one test covers multiple inputs/expected outputs.
- **Test discovery:**

  - Test files → must start with `test_` or end with `_test.py`.
  - Test functions/classes → must start with `test_`.

- **Naming** → clear test names help: `test_<function>_<condition>_<expected>()`.
- **Coverage** → tools like `pytest-cov` measure how much code is exercised.

#### Steps

1. **Setup fixtures**

   * Spin up a **test MongoDB** (could be a real ephemeral DB via `mongomock` or `testcontainers` Mongo).
   * Async `user_repo` fixture that points to the test DB.
   * Client fixture (`httpx.AsyncClient` + FastAPI `TestClient`) with dependency overrides to inject the test repo.

2. **Happy path test**

   * Send valid payload.
   * Assert `201 Created`.
   * Check DB actually has the new user with `is_verified=False`.
   * Response body matches `SuccessMessageResponse`.

3. **Duplicate user tests**

   * Insert a verified user before calling.
   * Send same username/email.
   * Assert `400` with `USER_EXISTS`.
   * Make sure the response never reveals whether it was username or email.

4. **Unverified user edge case** (the one you documented as a risk)

   * Insert an unverified user first.
   * Call register again.
   * Decide what your intended policy is: block, resend verification, or allow duplicate.
   * Assert behavior matches that policy.

5. **CSRF dependency**

   * Mock/fake `verify_csrf` dependency.
   * One test where it passes.
   * One test where it fails → expect `403`.

6. **Rate limit behavior**

   * Patch limiter to a test mode.
   * Flood requests and assert you eventually get `429 Too Many Requests`.

7. **DB failure simulation**

   * Monkeypatch `user_repo.find_verified` or `user_repo.insert` to raise an exception.
   * Assert endpoint returns `500` with your `InternalServerError`.

8. **Logging side-effects** (optional but nice in a mature suite)

   * Capture logs with `caplog`.
   * Assert certain log messages appear on success and failure paths.

#### DB related setup

1. **Separate DB**:

   * Use a dedicated test DB (like `myapp_test`).
   * Never touch prod or staging DBs.

2. **Empty at start**:

   * Tests don’t rely on preloaded prod data.
   * Each test either creates what it needs or you load a small fixture dataset.

3. **Isolation**:

   * Clean up after each test (truncate collections, rollback transactions, or use `delete_many({})`).
   * Ensures tests don’t leak state.

4. **Optional seeding**:

   * If many tests need the same baseline data (e.g. one admin user), seed it once in a fixture.
   * Keep it minimal and fake.

5. **Automation**:

   * CI/CD spins up the test DB automatically (often in Docker).
   * Dropped after tests finish.

### Other points to know

- no need to spin up uvicorn, pytest will do that for you.
  - it uses the `.env.test` file to set environment variables.
- tests will never touch the real DB. Instead, they use a test DB defined in `.env.test`.
- shared files like `conftest.py` and `mongo` are in the `tests/` folder.

### Types of Tests

* **Unit tests**

  * Isolate a single function or class.
  * Mock dependencies (e.g. repos, external services).
  * Fast, no DB.
  * **Simple/dumb** (minimal logic, easy to read).
  * Focused (test one behavior at a time).
  * Purpose: verify *logic correctness*.
  * Independent (shouldn't depend on order of execution).

* **Integration tests**

  * Use real DB (test Mongo instance).
  * Verify persistence, side-effects, and wiring.
  * Purpose: ensure *components work together*.

* **API/Functional tests**

  * Use FastAPI `TestClient`.
  * Hit endpoints over HTTP, assert status codes + payloads.
  * Purpose: verify *API contract*.

* (Optional later): regression, property-based, performance, security, etc.

### File Structure

Recommended pattern:

```
project/
  app/
    routes/
      auth.py
    repos/
      refresh_token_repo.py
  tests/
    unit/
      routes/
        test_auth.py              # unit tests for login (mock repo)
      repos/
        test_refresh_token_repo.py # unit tests for repo insert/find
    integration/
      test_auth_flow.py           # full login + token in DB
    functional/
      test_auth_api.py            # TestClient hitting /login
```

### Example: `login` Route

* **Unit** → mirror app structure.
* **Integration** → grouped by flow/feature.
* **Functional/API** → endpoint-focused.

```python
# app/routes/auth.py
@router.post("/login")
async def login(data: LoginRequest, repo: RefreshTokenRepo):
    user = await repo.find_user(data.username)
    if not user or not verify_pw(data.password, user.hashed_pw):
        raise HTTPException(401, "invalid creds")
    token = make_token(user.id)
    await repo.insert(token)
    return {"access": token}
```

#### Unit test (mock repo, test logic only)

```python
async def test_login_success(monkeypatch):
    repo = FakeRepo(user=User("u", "pw"))
    monkeypatch.setattr("app.routes.auth.make_token", lambda _: "tok")
    resp = await login(LoginRequest("u","pw"), repo)
    assert resp == {"access": "tok"}
```

#### Integration test (real DB, test side-effects)

```python
async def test_login_inserts_token(test_db, client):
    resp = client.post("/login", json={"username":"u","password":"pw"})
    assert resp.status_code == 200
    token = resp.json()["access"]
    # Check token is stored in Mongo
    doc = await test_db.tokens.find_one({"token": token})
    assert doc is not None
```

#### API/Functional test (focus on HTTP contract)

```python
def test_login_api(client):
    resp = client.post("/login", json={"username":"u","password":"pw"})
    assert resp.status_code == 200
    assert "access" in resp.json()
```

---

## FastAPI Background Tasks

if you want:

1. Send response right away
2. Run `foo()` after, but **not in a separate thread/process**

In FastAPI (or Starlette under the hood), the way to do this is with **background tasks**, not `yield`. Background tasks still run in the same process, just after the response is returned.

Example:

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def foo():
    print("running after response")

@app.get("/")
def home(background_tasks: BackgroundTasks):
    background_tasks.add_task(foo)
    return {"status": 200, "msg": "ok"}
```

What happens:

* Client gets `{"status": 200, "msg": "ok"}` immediately.
* Then FastAPI runs `foo()` right after finishing the response.
* No threading, no separate worker needed.

### yeild in FastAPI

Those don't go together.

In a **web route** (`@app.get("/")` in FastAPI):

* You just `return` something (dict, JSON, HTML, etc.).
* You **don’t** `yield` — unless you’re streaming responses.

Example FastAPI route:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": 200, "msg": "ok"}
```

If you actually wrote:

```python
@app.get("/")
def home():
    yield {"status": 200}
    foo()
```

What happens:

* FastAPI sees the `yield` → treats it like an async generator endpoint.
* The response will **stream out pieces** of data.
* `foo()` would run after sending the first chunk.

So `yield` inside routes = **streaming** (rarely what you want).

---