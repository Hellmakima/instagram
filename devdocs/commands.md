# Dev Setup Guide (_for myself_)

### Other Git Commands

```bash
git branch           # Check current branch
git branch -a        # List all branches
git branch devde     # Create new branch named 'devde'
git checkout devde   # Switch to branch 'devde'
# Merge/Pull via GitHub web interface
git branch -D devde  # Delete branch 'devde'
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
(venv)...\backend\auth-server> uvicorn app.main:app --reload --port 5001
(venv)...\backend\resource-server> uvicorn app.main:app --reload --port 5000
```
