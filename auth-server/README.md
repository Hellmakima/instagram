# InstaClone Auth Server

![Under Construction](https://raw.githubusercontent.com/sindresorhus/sindresorhus/main/under-construction.gif)

This file and the project are in the early stages of development.
We're currently in the process of separating this project into multiple repositories.

---

### Backend Dependencies installation

```bash
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
uv run uvicorn app.main:app --reload --port 5001
```

or

```bash
(venv) ~/auth-server$ uvicorn app.main:app --reload --port 5001
```

Each server has its swagger docs at `http://localhost:<port>/docs`.
