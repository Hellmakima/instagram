# TODO

_Search for `TODO` in all files to see all the todos_

## Ongoing Tasks

- complete the auth-server
  - add password change
- html for email verification

## High Priority

_Next steps_

- setup resource-server
- write tests for the project so far
- complete the resource-server repositories, models, services and endpoints
- setup redis for server communication
- capture user_agent and IP for refresh_tokens

## Upcoming **Waku-Waku**

_Exciting tasks_

- update python version to 3.14
- checkout new other flags for `uvicorn`.
- add health check endpoints
- make a YouTube video about this project
- add a simple user profile page and start looking into how to implement it.
  - DB schema, user images, etc
- need to think on what happens for multiple devices, a service to revoke all tokens, keep track of logged in devices, maybe add /revoke_all_by_user_id endpoint
- improve project documentation
  - verify requirements.txt by making a new venv and testing the project.
- a socket connection with the frontend to record last activity, realtime notifications, logout, etc.
- add basic pages such contact, about, etc. in the frontend
- make redux handle csrf, auth, etc.
- setup variables to use with tailwind
- format code with annotations

  eg:

  ```py
  async def foo(LoginForm: login_form) -> SuccessResponse:
    bool verified = is_verified(login_form)
    return SuccessResponse('You did good')
  ```

## Research

- [This](https://github.com/benavlabs/FastAPI-boilerplate) boilerplate is interesting.
- MVC structure
- `ruff` for linting
  - cd C:\Users\Sufiyan Attar\Documents\instagram\auth-server; py -m uv run ruff check .
  - or if ruff isn't installed:
  - cd C:\Users\Sufiyan Attar\Documents\instagram\auth-server; py -m uv run flake8 .
- see if we need `psutil` for health checks and other stuff
- learn `git rebase` specifically [squash](https://www.youtube.com/watch?v=gXCkYkLQ3To)
- in-memory sort operations in MongoDB
- Appropriate Database for each service.
  - For auth, file storage, maybe cassandra for linking between videos.
- IP validation helpers
- nginx vs traefik or others
  - Traefik is a **modern reverse proxy + load balancer** built for microservices and APIs.
    - It sits in front of your apps (like Nginx/HAProxy would) and routes traffic.
    - Auto-discovers services from Docker, Kubernetes, or your config.
    - Handles SSL certs automatically via Let’s Encrypt.
    - Supports sticky sessions, load balancing, middleware (rate limiting, auth, etc.).
    - Popular in containerized setups since you don’t need to manually edit configs when services come/go.
- See how docker-compose is setup
  - for dev, stage, prod
  - for Mongo/Postgres/Redis with multiple connections (user, pass)
  - dependabot for updating dependencies
  - redis as communication between services (master + replica), individual for each service for rate limiting

## Read

- [FastAPI Test setup](https://testdriven.io/blog/fastapi-crud/)
- look up [fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- [fastapi-motor-mongo-template](https://github.com/alexk1919/fastapi-motor-mongo-template)
- [api-testing-masterclass](https://github.com/Pytest-with-Eric/api-testing-masterclass)

## Medium Priority Tasks

- logo animation
- implement more from [Auth-server](https://github.com/hellmakima/instagram/blob/main/auth-server/app/api/structure.md)
- setup separate repositories for each server
- get resource-server running.
- Create a DatabaseProtocol or abstract interface for every database method (find_one, insert_one, delete_many, etc.) and use it in the repositories and the apis. Won't be doing this for auth-server, but it will be for the other services.
- update `devdocs/file_structure.ini` with new structure.
- email verification
- start versioning
- TTL stuff
  - Add Mongo TTL for refresh tokens
  - Add TTL for is_suspended
    - put blocked_till field in user schema and make a service to unblock users every X days.
  - same for is_pending_deletion
    - but here the enty moves to a separate collection with PII removed.
- redo cookie setting, add samesite, httponly, secure, path, domain, etc once respective frontend is done.
- use `pytest-cov`
- add password related endpoints (change password, forgot password, reset password)
- add user related endpoints (create user, delete user, update user)
- Require re-authentication for key operations (email changes, MFA toggles).
- switch to `PostgreSQL` once close to stable.
- move to python 3.14 once all the build-wheels are available.
- lockouts, CAPTCHA, MFA.
- logout
  - move it to new folder `auth-server/app/api/api_v1/logout/router.py`
  - store `user agent` and `ip` in `refresh_tokens` collection.
  - let user logout from other devices and potentially other services.
  - also maybe `logout_all_devices` endpoint.

## Ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors
- update requirements.txt
- run `uv format`
- run `schemathesis run --checks all --url http://localhost:5001 openapi.json`
  - `openapi.json` is the path to the openapi.json file (found at `localhost:5001/openapi.json`)
- code review
  - proper logging for FE and BE
  - error handling
  - type checking
  - rate limiting for each endpoint
  - add docstrings
  - clean up
    - remove unused imports
    - remove commented code or comments
    - format code
    - remove trailing whitespace

## Low Priority Tasks

- separate repository for each server
- use `requirements.txt` for prod, `requirements-dev.txt` for pytest/locust/dev tools for each server.
- try out [fastapi-cli](https://github.com/fastapi/fastapi-cli) and [SQLModel](https://github.com/fastapi/sqlmodel) for ORM.
- or maybe go [SQL-only](https://www.youtube.com/watch?v=bpGvVI7NM_k) without an ORM with t-strings.
- setup nginx
  - rate limiting
  - route with subdomains
  - add CORS headers
  - other things that nginx can do:
    - SSL termination
    - static file serving
    - load balancing
    - caching

## Eventually

- Make files:
  - Makefile
    - dev: run app with auto-reload
    - run: run app in prod mode
    - test: run pytest
    - lint: run lint checks
    - clean: clear caches (pycache, pytest_cache, etc)
  - docker-compose.yml
- set up a protection against DDOS attacks. Maybe new custom captcha that kick in during high traffic.
- set refresh tokens only if user wants to
- Look into `gunicorn` + `uvicorn.workers.UvicornWorker`, or using `uvicorn` and `gunicorn` together.
- use a Python profiler (like `py-spy` or `cProfile`) on your running FastAPI application during load testing. This will show you exactly which lines of code are consuming the most CPU time.
- For an Instagram clone, which can scale significantly, I would strongly recommend considering a dedicated API Gateway solution (e.g., Kong, Apache APISIX, etc.) to handle all the traffic.
- Use Redis insted of get_current_user() if that becomes a bottleneck.

## Before Deployment

- use proper license, security.md, code_of_conduct.md
- put new environment variables
- remove CORS, use nginx to bring it all together
- for docker refer [Youtube](https://www.youtube.com/watch?v=DQdB7wFEygo)
- deploy!!! Even temporarily, just do it
