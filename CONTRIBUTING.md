# Contributing Guidelines

## Build Principles

- Refer [this](https://github.com/hellmakima/instagram/blob/main/devdocs/build_principles.md) for more details.

## Coding Standards

- No Python file >750 lines. No function >75 lines.
- Use logging. Never use `print` or `global`.
- No unused imports.
- Code must be readable even if you don't know Python. Write comments if unclear.
- Occasionally enable `python.analysis.typeCheckingMode` in VSCode.

---

## Testing

- Use Swagger UI at `/docs`.
- Start with `static/index.html` for early backend testing.
- Load test via Locust (`/test/locust_test.py`, port 8089).
- Use `pytest` for unit tests.

## Git Workflow

- Don't push to `main`. Period.
- All your branches should be named `username/module-name/feature-name`. For example, `tojifushiguro/shops/analytics-dashboard`.
- Same format for commit messages.
- Use `git rebase` to squash commits before merging to `main`.
- [PR template](https://github.com/hellmakima/instaclone/blob/main/d:/project/instagram/PULL_REQUEST_TEMPLATE.md)
