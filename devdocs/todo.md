"""

### File: **project/todo.md**

Contains the todo list for the project
"""

# TODO

_Search for `TODO` in all files to see all the todos_

## High Priority

- add a simple user profile page and start looking into how to implement it.
  - DB, session, etc
  or
- go with email verification and password reset
- decide DB struct and indexes

## Research

- CSRF tokens, proper location to store the access nad refresh tokens. see how real instagram does it, look up git repos for implementation, and tatakae
- data validation on frontend as well as backend?
- do we need redis for session storage?
- IP validation helpers
- https://fusionauth.io/blog/understanding-oauth2-grant-types multiple servers to handle different services. Allows third party apps to use instagram without having to implement their own login system
- make sure token validation speed scales (consider caching JWT validation results short-term to reduce auth server hits

## Medium Priority

- need a good blacklist/rotation strategy for refresh tokens
  - Mongo TTL index maybe
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

## ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors

## eventually

- Add rate-limiting to critical endpoints
- Add proper logging
- I use models dir for validation. mabe fix this
- set up a common page for 404 page not found
- set refresh tokens only if user wants to
- Look into `gunicorn` + `uvicorn.workers.UvicornWorker`
- use a Python profiler (like `py-spy` or `cProfile`) on your running FastAPI application during a login request. This will show you exactly which lines of code are consuming the most CPU time
-  For an Instagram clone, which can scale significantly, I would strongly recommend considering a dedicated API Gateway solution (e.g., Kong, Apache APISIX,
