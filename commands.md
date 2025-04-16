# Dev Setup Guide (_for myself_)

## Git Workflow

### Login with Git GUI

### Always Pull First
```bash
git pull origin main
```

### When Updating
```bash
git add .
git commit -m "your message"
git push origin main
# main is the branch name
```

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

_Runs on port 3000_

### First Run
```bash
npm install
npm run dev
```

### Run Code
```bash
npm run dev
# Ctrl+C to stop
```

---

## Backend

### First Run
py 3.13.2
```bash
py -m venv "env_name"
"env_name"\Scripts\Activate
pip install -r pip_requirements.txt
uvicorn main:app --reload --port 5000
```

### Run Code
```bash
"env_name"\Scripts\Activate
uvicorn main:app --reload --port 5000
# Ctrl+C to stop
```

---

## Cloudflared

```bash
cloudflared tunnel --url http://localhost:5000
```

---

## New NextJS App

```bash
npx create-next-app@latest frontend
```

---

## Setup Tools for REST

### VS Code
1. Install `REST Client` extension.
2. Open/create a `.rest` or `.http` file.
3. Click `Send Request`.

### Sublime Text 4
1. Check version (`Help -> About`).
2. Get `Package Control` via `Ctrl+Shift+P`.
3. Install `REST Client` using `Package Control: Install Package`.
4. Set up key binding:
```json
{ "keys": ["your_key_binding"], "command": "rest_request" }
```
5. Or run via `Ctrl+Shift+P` → `REST Client: Send request`.