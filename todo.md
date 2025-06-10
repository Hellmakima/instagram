"""
### File: **project/todo.md**

Contains the todo list for the project
"""

# TODO

## High Priority

- once done with token stuff, add a simple user profile page and start looking into how to implement it (DB, session, etc)
  or
- go with email verification and password reset

## Research

- CSRF tokens, proper location to store the access nad refresh tokens. see how real instagram does it, look up git repos for implementation, and tatakae
- data validation on frontend as well as backend?
- do we need redis for session storage?
- IP validation helpers

## Medium Priority

- make a index page to list all the endpoints
- add password related stuff [change password, forgot password, reset password]
- add user related stuff [create user, delete user, update user]
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

- remove CORS
- nginx to bring it all together
- use docker
  - separate container
  - refer [Youtube](youtube.com/watch?v=DQdB7wFEygo)
- test on wsl
- deploy!!!

## ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors

## eventually

- Add rate-limiting to critical endpoints
- Add proper logging
- I use models dir for validation. mabe fix this
- set up a common page for 404 page not found
- set refresh tokens only if user wants to
