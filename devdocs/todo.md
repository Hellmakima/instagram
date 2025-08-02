"""

### File: **project/todo.md**

Contains the todo list for the project
"""

# TODO

_Search for `TODO` in all files to see all the todos_

## High Priority

- make static pages and test auth-server
- get resource-server running
- add a simple user profile page and start looking into how to implement it.
  - DB schema, etc
- go with email verification and password reset

## Research

- data validation on frontend as well as backend?
- IP validation helpers
- https://fusionauth.io/blog/understanding-oauth2-grant-types multiple servers to handle different services. Allows third party apps to use instagram without having to implement their own login system

## Medium Priority

- need a good blacklist/rotation strategy for refresh tokens
  - Mongo TTL index maybe
- redo cookie setting, add samesite, httponly, secure, path, domain, etc
- make a index page to list all the endpoints
- add password related stuff [change password, forgot password, reset password]
- add user related stuff [create user, delete user, update user]
- Require re-authentication for key operations (email changes, MFA toggles).
- implement rate-limiting, lockouts, CAPTCHA, MFA.
- add user-specific endpoints
  - get user info
  - block user
  - unblock user
  - delete user
  - update user
    - update user password
    - update user data
- setup nginx

  - rate limiting
  - route with subdomains
  - add CORS headers

  ```
    if host.startswith("auth."):
        "http://127.0.0.1:5001"
    elif host.startswith("api."):
        "http://127.0.0.1:5002"
  ```

  - other things that nginx can do:
    - SSL termination
    - rate limiting
    - static file serving
    - basic reverse proxying
    - basic cors headers
    - load balancing
    - caching

## Low Priority

- Store refresh tokens server-side (in DB). Add blacklisting logic to refresh tokens on logout and stuff
  - add req logs for imp endpoints with source IP

## Before Deployment

- use proper license, security.md, code_of_conduct.md
- rewrite gitignore and put new values in .env
- remove CORS, use nginx to bring it all together
- use docker
  - separate container
  - refer [Youtube](youtube.com/watch?v=DQdB7wFEygo)
- test on wsl
- deploy!!! Even temporarily, just do it

## Ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors

## Eventually

- I use models dir for validation. mabe fix this
- set up a common page for 404 page not found (do it in the frontend)
- set refresh tokens only if user wants to
- Look into `gunicorn` + `uvicorn.workers.UvicornWorker`
- use a Python profiler (like `py-spy` or `cProfile`) on your running FastAPI application during a login request. This will show you exactly which lines of code are consuming the most CPU time
- For an Instagram clone, which can scale significantly, I would strongly recommend considering a dedicated API Gateway solution (e.g., Kong, Apache APISIX,
- Use Redis insted of get_current_user() if that becomes a bottleneck.
