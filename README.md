<h1 align="center">﷽</h1>

# InstaClone

A full-stack Instagram-like application built using **FastAPI**, **MongoDB**, and **Next.js**.
Designed with modularity, clarity, and scalability in mind.

![Under Construction](https://raw.githubusercontent.com/sindresorhus/sindresorhus/main/under-construction.gif)

This file and the project are in the early stages of development.
We're currently in the process of separating this project into multiple repositories.

---

### Backend Dependencies installation

```bash
cd instagram
uv sync --frozen
```

or

```bash
pip install -r ./instagram/devdocs/requirements.txt
```

or

install from [pips.md](https://github.com/hellmakima/instagram/blob/main/devdocs/pips.md) one by one.

### Run the Servers

```bash
/instagram/auth-server$ uv run uvicorn app.main:app --reload --port 5001
```

or

```bash
(venv) ~/instagram/auth-server$ uvicorn app.main:app --reload --port 5001
```

Each server has its swagger docs at `http://localhost:<port>/docs`.

---

## Contributors & Tools

- [Supermaven VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Supermaven.supermaven) - Massive shoutout to for unlimited free fancy auto-completions.
- [Gemini](https://gemini.google.com/app?hl=en-IN) - Great teacher after some tweaking.
- [ChatGPT](https://chatgpt.com/?temporary-chat=true) - For any small tasks and questions.

---

## Author

Developed by [@hellmakima](https://github.com/hellmakima)

---

Pull requests, suggestions, and collaborations are welcome.
