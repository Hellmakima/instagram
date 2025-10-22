<h1 align="center">﷽</h1>

# <img src="https://github.com/Hellmakima/instagram/raw/main/frontend/public/favicon.ico" alt="favicon" width="32" height="32"> Nmaa (نما)

A full-stack Instagram-like application built using **FastAPI**, **MongoDB**, and **Next.js**
Designed with modularity, clarity, and scalability

This project is currently in the early stages of development.

---

## Features

- **Microservices Architecture** – Modular Auth and Resource servers
- **JWT Auth & Refresh Tokens** – Secure authentication and session management
- **Async FastAPI** – Non-blocking I/O and dependency injection
- **Redis Caching** – In-memory performance optimization
- **MongoDB (Motor)** – Async NoSQL document database
- **Next.js (TypeScript)** – Modern frontend with Tailwind, Redux Toolkit, and Shadcn UI
- **Docker Support** – Ready for containerized deployment

---

## Tech Stack

| Layer          | Tech                                                            |
| -------------- | --------------------------------------------------------------- |
| Backend        | FastAPI, Motor, Redis, Pydantic, bcrypt                         |
| Frontend       | Next.js, TypeScript, TailwindCSS, Redux Toolkit, Shadcn, lucide |
| Infrastructure | Docker, Caddy (reverse proxy), MongoDB                          |
| Testing & Dev  | pytest, VS Code Tasks                                           |

---

## Getting Started

This project has a multi-server architecture, each server has its own folder (`auth-server`, `resource-server`, and `frontend`).

```bash
git clone https://github.com/hellmakima/instagram.git
```

**Note:** Some critical files might be hidden, please check .vscode/settings.json for the correct settings.

<details>
  <summary><b>Auth Server</b></summary>

The auth server is responsible for user authentication, password management, and user management.
It uses JWT for authentication and refresh tokens for session management.

**MongoDB**
Database: `instagram_auth`

```bash
cd instagram/auth-server
uv sync --frozen
uv run uvicorn app.main:app --reload --port 5001
```

</details>

<details>
  <summary><b>Resource Server</b></summary>

The resource server handles all media files and their metadata.

**MongoDB**
Database: `instagram_resource`

```bash
cd instagram/resource-server
uv sync --frozen
uv run uvicorn app.main:app --reload --port 5002
```

</details>

<details>
  <summary><b>Gateway Server</b></summary>

This is a reverse proxy that routes all frontend requests to the correct backend server.
Currently implemented with **Caddy**, but will later be replaced by **nginx**.

You can skip this and configure `instagram/frontend/.env` to proxy requests directly, along with setting proper CORS headers in each server’s `main.py`.

**Setup:**

1. Download [Caddy Server](https://caddyserver.com/download)
2. Copy `instagram/utils/caddy.json` to the same folder
3. Run:

   ```bash
   caddy_windows_amd64.exe run
   ```

4. In a new terminal:

   ```bash
   caddy_windows_amd64.exe reload --config caddy.json
   ```

**Hosts Configuration (Windows):**
Edit `C:\Windows\System32\drivers\etc\hosts`:

```
127.0.0.1 nmaa.com
127.0.0.1 auth.nmaa.com
127.0.0.1 resource.nmaa.com
```

</details>

<details>
  <summary><b>Frontend</b></summary>

The frontend is a **Next.js** application.

```bash
cd instagram/frontend
npm i
npm run dev
```

Then visit `nmaa.com` in your browser.

</details>

<details>
  <summary><b>Tests</b></summary>

Each server contains tests in its `test` folder.
Run them using:

```bash
uv run pytest
```

</details>

---

## Author

Developed by [@hellmakima](https://github.com/hellmakima)

---

Pull requests, suggestions, and collaborations are welcome.
