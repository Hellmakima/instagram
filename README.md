<h1 align="center">﷽</h1>

# Instagrm Clone (Full-Stack Instagram-like Application)

A full-stack Instagram-like application built using **FastAPI**, **MongoDB**, and **Next.js**
Designed with modularity, clarity, and scalability in mind

This project is currently in the early stages of development and is being prepared for migration into a microservices architecture across multiple repositories

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Auth Server](#auth-server)
  - [Resource Server](#resource-server)
  - [Gateway Server](#gateway-server)
  - [Frontend](#frontend)
- [Contributors & Tools](#contributors--tools)
- [Author](#author)

---

## Features

- Microservices Architecture: Separate Auth and Resource servers
- JWT Authentication and Refresh Token management
- Automatic Swagger/OpenAPI documentation for each server
- Built with FastAPI, MongoDB, and Next.js for a modern, high-performance stack
- Asynchronous backend design for high concurrency and I/O efficiency
- Rate Limiting implemented on the Auth Server to prevent abuse and brute-force attacks
- CORS headers implemented on the Frontend to allow requests from any origin
- Type-safe development using TypeScript on the frontend and Pydantic/type hints on the backend

---

## Getting Started

This project has a multi-server architecture, so it's supposed to be in multiple repositories, but for now, we're keeping it all in one. Each server has its own folder

So you get all the servers by cloning this repository

```bash
git clone https://github.com/hellmakima/instagram.git
```

I'm using [uv](https://github.com/astral-sh/uv) package manager instead of `pip` and `venv`. You can install dependencies with `pip` using `instagram/devdocs/requirements.txt` or one by one with `instagram/devdocs/pips.txt`

Sorry for also including `.vscode` folder, but it has tasks setup that you can use to run the servers

### Auth Server

The auth server is responsible for user authentication, password management, and user management
It uses JWT for authentication and refresh tokens for session management

**MongoDB**
Database: instagram_auth
Collections: users, refresh_tokens

```bash
cd instagram/auth-server
uv sync --frozen
uv run uvicorn app.main:app --reload --port 5001
```

### Resource Server

The resource server is responsible for handling all the media files and their metadata

**MongoDB**
Database: instagram_resource
Collections: users

```bash
cd instagram/resource-server
uv sync --frozen
uv run uvicorn app.main:app --reload --port 5002
```

### Gateway Server

This is reverse proxy for handling all the requests from the frontend and redirecting them to the appropriate server

This is just a temporary solution to redirect requests. This will be replaced by `nginx`

You can skip this and configure `instagram/frontend/.env` to proxy requests to the appropriate server along with CORS headers in main.py of respective server

1. Download [caddyserver](https://caddyserver.com/download)
2. copy `instagram/utils/caddy.json` to the same folder
3. run `caddy_windows_amd64.exe run`
4. in a new terminal, run `caddy_windows_amd64.exe  reload --config caddy.json`

You'll also need to set up `hosts` file in `C:\Windows\System32\drivers\etc` with the following content:

```
127.0.0.1 nmaa.com
127.0.0.1 auth.nmaa.com
127.0.0.1 resource.nmaa.com
```

### Frontend

The frontend is a Next.js application

```bash
cd instagram/frontend
npm i
npm run dev
```

You're all set!
visit `nmaa.com` in your favorite browser

## Contributors & Tools

- [Supermaven VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Supermaven.supermaven) - Massive shoutout to for unlimited free fancy auto-completions
- [Gemini](https://gemini.google.com/app?hl=en-IN) - Great teacher after some tweaking
- [ChatGPT](https://chatgpt.com/?temporary-chat=true) - For any small tasks and questions

---

## Author

Developed by [@hellmakima](https://github.com/hellmakima)

---

Pull requests, suggestions, and collaborations are welcome
