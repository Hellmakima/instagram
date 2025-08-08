"""

### File: **project/todo.md**

Contains the todo list for the project
"""

# TODO

_Search for `TODO` in all files to see all the todos_

## High Priority

- get resource-server running.
- add a simple user profile page and start looking into how to implement it.
  - DB schema, user images, etc

## Research

- data validation on frontend as well as backend?
- IP validation helpers
- https://fusionauth.io/blog/understanding-oauth2-grant-types multiple servers to handle different services. Allows third party apps to use instagram without having to implement their own login system

## Medium Priority

- email verification
- Add Mongo TTL for refresh tokens
- redo cookie setting, add samesite, httponly, secure, path, domain, etc once respective frontend is done.
- add password related endpoints [change password, forgot password, reset password]
- add user related endpoints [create user, delete user, update user]
- Require re-authentication for key operations (email changes, MFA toggles).
- lockouts, CAPTCHA, MFA.

## Low Priority

- setup nginx
  ```
    if host.startswith("auth."):
        "http://127.0.0.1:5001"
    elif host.startswith("api."):
        "http://127.0.0.1:5002"
  ```
  - rate limiting
  - route with subdomains
  - add CORS headers
  - other things that nginx can do:
    - SSL termination
    - static file serving
    - load balancing
    - caching

## Ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors
- update requirements.txt

## Eventually

- set refresh tokens only if user wants to
- Look into `gunicorn` + `uvicorn.workers.UvicornWorker`
- use a Python profiler (like `py-spy` or `cProfile`) on your running FastAPI application during load testing. This will show you exactly which lines of code are consuming the most CPU time.
- For an Instagram clone, which can scale significantly, I would strongly recommend considering a dedicated API Gateway solution (e.g., Kong, Apache APISIX, etc.) to handle all the traffic.
- Use Redis insted of get_current_user() if that becomes a bottleneck.

## Before Deployment

- use proper license, security.md, code_of_conduct.md
- rewrite gitignore and put new values in .env
- remove CORS, use nginx to bring it all together
- use docker
  - separate container
  - refer [Youtube](youtube.com/watch?v=DQdB7wFEygo)
- test on wsl
- deploy!!! Even temporarily, just do it