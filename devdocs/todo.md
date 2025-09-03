# TODO

_Search for `TODO` in all files to see all the todos_

## High Priority Tasks

- make a layer between all servers and the database
- add a simple user profile page and start looking into how to implement it.
  - DB schema, user images, etc
- implement better documentation for code
- write tests for the project so far
  - remove warnings that show up on pytest
  - clone (fastapi-motor-mongo-template)[https://github.com/alexk1919/fastapi-motor-mongo-template] and use it as a reference
- improve project documentation
  - verify requirements.txt by making a new venv and testing the project.

## Research

- MVC structure
- ORM
- see if we need `psutil`
- in-memory sort operations in mongodb
- look up [fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
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

  Think of it as **“Nginx, but built for dynamic cloud-native environments.”**

## Medium Priority Tasks

- get resource-server running.
- update `devdocs/file_structure.ini` with new structure.
- email verification
- TTL stuff
  - Add Mongo TTL for refresh tokens
  - Add TTL for is_blocked
    - put blocked_till field in user schema and make a service to unblock users every X days.
  - same for is_deleted
    - but here the enty moves to a separate collection with PII removed.
- redo cookie setting, add samesite, httponly, secure, path, domain, etc once respective frontend is done.
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

- separate repository for frontend
- setup nginx

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
  - Dockerfile
  - docker-compose.yml
  - pyproject.toml
  - uv.yaml
- set refresh tokens only if user wants to
- Look into `gunicorn` + `uvicorn.workers.UvicornWorker`, or using `uvicorn` and `gunicorn` together.
- see if we can use `pip install cookiecutter` to generate our project
- try `uv` package manager instead of `pip` and `venv`
- use a Python profiler (like `py-spy` or `cProfile`) on your running FastAPI application during load testing. This will show you exactly which lines of code are consuming the most CPU time.
- For an Instagram clone, which can scale significantly, I would strongly recommend considering a dedicated API Gateway solution (e.g., Kong, Apache APISIX, etc.) to handle all the traffic.
- Use Redis insted of get_current_user() if that becomes a bottleneck.

## Before Deployment

- use proper license, security.md, code_of_conduct.md
- rewrite gitignore and put new values in .env
- remove CORS, use nginx to bring it all together
- test on wsl
- use docker
  - separate container
  - refer [Youtube](https://www.youtube.com/watch?v=DQdB7wFEygo)
- deploy!!! Even temporarily, just do it
