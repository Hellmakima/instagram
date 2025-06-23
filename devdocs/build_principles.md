# Build Principles

## Servers

- 2 servers (auth 5001 and resources 5000)
  - Auth server acts as a proxy for the resources server. Frontend only sees the resources server. Any requests that require auth are proxied to the auth server.
  - Auth server implements OAuth2 protocol to allow third-party apps to access the resources server with limited access granted by the user.
  - Auth server is stateless, and doesn't store any user data.
- common virtual environment
- Most operations are async
- Shared user \_id passed in token for cross-server consistency

## API

- RESTful API used for all operations
- JWT passed as Authorization: Bearer <token> header in secured routes

## Authentication

- OAuth2 protocol
  - Implemented access token and refresh token
  - Also CSRF token
  - JWT signed w/ HS256
  - Tokens validated with type, sub, and exp checks
- Passwords hashed using bcrypt via passlib

## Database

- NoSQL
- Try to keep it modular, tiny collections
- Each server has its own collection in a shared database to later be split into separate databases

## Frontend

- Pure vibe coding.
- SPA (single page app)
- Use any copyrighted images, fonts, etc.

## Testing

- Swagger UI (http://localhost:5000/docs) to test APIs.
- Before making pages, make static html (project/backend/static/index.html) to test the backend.
- Locust (/backend/test/locust_test.py) for load testing.

## Proxy

- reverse proxy used to host the frontend and backend

## Future Add-ons

- Rate limiting via Redis or API Gateway
- User scopes/roles (admin, mod, etc.) for granular access control
- Webhooks for auth events (login, logout, password reset)
- Email & phone verification (via OTP)
