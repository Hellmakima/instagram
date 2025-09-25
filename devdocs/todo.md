# TODO

_Search for `TODO` in all files to see all the todos_

## High Priority/Current Tasks

- write tests for the project so far
  - clone (fastapi-motor-mongo-template)[https://github.com/alexk1919/fastapi-motor-mongo-template] and use it as a reference
- setup separate repositories for each service
- mTLS or API key for internal communication

## Upcomming **Waku-Waku**

- design a logo for the app. The logo must comply with the following rules:
  - Vector design, square format
  - Works in both light & dark mode
  - Recognizable even when pixelated
  - Animated
  - Symbolizes growth, privacy, and security
  - Color palette applied
  - I'm thinking sequoia seed or sapling as a logo
- add health check endpoints
- make a youtube video about this project
- add a simple user profile page and start looking into how to implement it.
  - DB schema, user images, etc
- improve project documentation
  - verify requirements.txt by making a new venv and testing the project.
- format code with annotations
  - eg:
  ```py
  async def foo(LoginForm: login_form) -> SuccessResponse:
    bool verified = is_verified(login_form)
    return SuccessResponse('You did good')
  ```
- use `uv` package manager instead of `pip` and `venv` after getting python 3.14

## Research

- MVC structure
- ORM
- see if we need `psutil` for health checks and other stuff
- learn `git rebase` specifically [squash](https://www.youtube.com/watch?v=gXCkYkLQ3To)
- in-memory sort operations in mongodb
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

## Read

- [FastAPI Test setup](https://testdriven.io/blog/fastapi-crud/)
- look up [fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- [fastapi-motor-mongo-template](https://github.com/alexk1919/fastapi-motor-mongo-template)
- [api-testing-masterclass](https://github.com/Pytest-with-Eric/api-testing-masterclass)

## Medium Priority Tasks

- get resource-server running.
- Create a DatabaseProtocol or abstract interface for every database method (find_one, insert_one, delete_many, etc.) and use it in the repositories and the apis. Won't be doing this for auth-server, but it will be for the other services.
- update `devdocs/file_structure.ini` with new structure.
- email verification
- start versioning
- TTL stuff
  - Add Mongo TTL for refresh tokens
  - Add TTL for is_blocked
    - put blocked_till field in user schema and make a service to unblock users every X days.
  - same for is_deleted
    - but here the enty moves to a separate collection with PII removed.
- redo cookie setting, add samesite, httponly, secure, path, domain, etc once respective frontend is done.
- use `pytest-cov`
- add password related endpoints [change password, forgot password, reset password]
- add user related endpoints [create user, delete user, update user]
- Require re-authentication for key operations (email changes, MFA toggles).
- lockouts, CAPTCHA, MFA.

## Ocassionally

- search python.analysis.typeCheckingMode in VSCode and enale to look up potential errors
- update requirements.txt
- code review
  - look for proper logging
  - error handling
  - type checking
  - look for what can be a bottleneck for scalability

## Low Priority Tasks

- separate repository for each server
- use `requirements.txt` for prod, `requirements-dev.txt` for pytest/locust/dev tools for each server.
- setup nginx

  - look into `nginx config.md`

  ```python
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
