"""
File: **project/todo.txt**

Contains the todo list for the project
"""

# TODO

## High Priority

- add CORS during development and remove it before deploying
- add logs everywhere
- add logout endpoint + update static files
- Store refresh tokens server-side (in DB). Add blacklisting logic to refresh tokens
- make nextjs pages for login, register, and profile
- remove requests logger

## Research

- data validation on frontend as well as backend?

## Medium Priority

- clean api_tesr.rest
- add rate-limiting to /login endpoint
- look up "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1"
- make nextjs pages for login, register, and profile
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

Add rate-limiting to /login endpoint
add "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" if you feel like it
