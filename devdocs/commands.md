# Dev Setup Guide (_for myself_)

### Other Git Commands

```bash
git commit -a -m "message" # Commit all changes
git branch           # Check current branch
git branch -a        # List all branches
git branch dev     # Create new branch named 'dev'
git checkout dev   # Switch to branch 'dev'
# Merge/Pull via GitHub web interface
git branch -D dev  # Delete branch 'dev'
```

---

## Frontend

### First Run

```bash
npm i
npm run dev
```

---

## New NextJS App

```bash
npx create-next-app@latest frontend
```

---

## Backend

```bash
# run the server
uv run uvicorn app.main:app --reload --port 5000
# run the tests
pytest
```

if you get an error like ImportError or ModuleNotFoundError, try this:

```powershell
(venv) ~\backend\auth-server> $env:PYTHONPATH = "D:\project\instagram\backend\auth-server"
(venv) ~\backend\auth-server> pytest
```
