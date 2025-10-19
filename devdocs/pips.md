## Auth server dependencies:

Add packages with `pip install <package-name>` or `uv add <package-name>`

**Production:**
bcrypt==3.2.0 # for password hashing
fastapi # for APIs
fastapi-csrf-protect # for CSRF protection
motor # for MongoDB connection
passlib[bcrypt]==1.7.4 # for password hashing
pydantic[email]
python-jose[cryptography] # for JWT
python-json-logger # for logging
slowapi # for rate limiting
uvicorn[standard] # for running the app, if failed to install then do uvicorn or use gunicorn

**Development:**
pytest
pytest-asyncio # for async tests eg: motor
pytest-dotenv # for loading .env.test variables
pytest-mock # for mock objects
httpx

---

# for gate.py (temporary)

httpx # for making HTTP requests to downstream services

## for utilities

locust # for load testing
python-multipart # for file uploads
