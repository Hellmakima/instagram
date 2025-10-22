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
git tag <tag_name># create a tag
git tag -f <tag_name> <commit_hash> # Force create a tag for a specific commit
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

## Public and private keys creation

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

Paste the keys in the `.env` file. Use quotes and put `\n` for each line.

**Note:** The private key should be kept private and never shared.
I have shared mine with you, but you should never.

## .env.enc file

- Encrypt the `.env` file

```bash
py .\utils\cerberus.py encrypt --infile <path_to_env_file> --outfile <path_to_encrypted_env_file>
```

```bash
py .\utils\cerberus.py decrypt --infile <path_to_encrypted_env_file> --outfile <path_to_env_file>
```
