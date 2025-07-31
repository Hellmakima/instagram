# Contributing Guidelines

## Build Principles

### Servers

- **Gateway Server**: Handles CSRF, request forwarding, and (TODO) rate limiting.
- **Auth Server (5001)**: Proxies auth requests, implements OAuth2, stateless.
- **Resource Server (5000)**: Main app logic. Frontend only talks to this.

### Architecture

- Auth server proxies to resource server for authenticated requests.
- JWT used for stateless auth; shared user ID across servers.
- CSRF handled by gateway using `fastapi-csrf-protect`.

---

## Coding Standards

- Use a shared virtual environment.
- Prefer `async` for all I/O.
- No Python file >750 lines. No function >75 lines.
- Use logging. Never use `print` or `global`.
- No unused imports.
- Code must be readable. Write comments if unclear.
- Occasionally enable `python.analysis.typeCheckingMode` in VSCode.

---

## API Design

- RESTful API.
- Support API versioning. Always keep backwards compatibility.

### Standard Success Response

```json
{
  "status": "success",
  "message": "Post created successfully",
  "code": 201,
  "data": {...},
  "timestamp": "2025-06-23T15:35:00Z"
}
```

### Standard Error Response

```json
{
  "status": "error",
  "message": "User not found",
  "code": 404,
  "details": {...},
  "timestamp": "2025-06-23T15:30:00Z"
}
```

- JWT is passed via `Authorization: Bearer <token>`.

#### Why Version APIs?

- Handles multi-client use (mobile, CLI, etc.).
- Allows graceful rollout and deprecation.
- Debugging is easier by version.
- Prevents breaking queued or long-lived requests.
- Supports rolling deploys safely.

---

## Authentication

- OAuth2 via JWT (HS256).
- Access + refresh tokens in `SameSite=Strict` cookies.
- CSRF managed by gateway; checked on all requests.
- Passwords hashed via bcrypt (passlib). Never store raw passwords.

---

## Database

- NoSQL (MongoDB, port 27017).
- Use modular, small collections.
- Each server has its own collection.

---

## Frontend

- SPA on port 3000.
- Built with NextJS. May migrate to Vite + React.
- Pure vibes. Any images/fonts are fair game.

---

## Testing

- Use Swagger UI at `/docs`.
- Start with `static/index.html` for early backend testing.
- Load test via Locust (`/test/locust_test.py`, port 8089).

---

## Networking

- Use reverse proxy for shared domain.
- Always use `cloudflared`. Never ngrok.

---

## Git Workflow

- Don't push to `main`. Period.
- Everything else: do what you want.

---

## Future Plans

- Add user scopes/roles (admin, mod, etc.).
- Email/phone OTP verification.
- All HTTP/HTTPS for now; WSS to be isolated when added.
- Sanitize all user input (XSS prevention, etc.).
