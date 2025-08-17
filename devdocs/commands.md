# Dev Setup Guide (_for myself_)

### Other Git Commands

```bash
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

### Run

```bash
(venv) ~/backend/gate> uvicorn main:app --reload --port 5000
(venv) ~/backend/auth-server> uvicorn app.main:app --reload --port 5001
```
