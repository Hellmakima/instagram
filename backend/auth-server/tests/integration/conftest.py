# # tests/integration/conftest.py
# # This configures the pytest environment for integration tests.
# # These hit the actual endpoints and database (instagram_test) with async requests.

# import os
# import pytest
# import pytest_asyncio
# from dotenv import load_dotenv
# from app.main import app as fastapi_app
# from ..mongo_client import TestMongoClient
# from httpx import AsyncClient, ASGITransport

# load_dotenv(dotenv_path=".env.test", override=True)



# @pytest.fixture(scope="session")
# def app():
#     return fastapi_app


# @pytest_asyncio.fixture()
# async def mongo_client():
#     async with TestMongoClient(
#         os.getenv("MONGODB_DBNAME", "instagram_test"),
#         os.getenv("MONGODB_USERS_COLLECTION", "users")
#     ) as mongo:
#         yield mongo


# @pytest_asyncio.fixture()
# async def async_client(app, mongo_client):
#     """
#     This sets client for rest of the tests
#     """
#     app.state.client = mongo_client
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         yield client
#     """
#     TODO: change this fixture to use asgi_lifespan. coz currently it is more manual.
#     ```py
#     from asgi_lifespan import LifespanManager
#     from httpx import AsyncClient, ASGITransport
#     import pytest_asyncio

#     @pytest_asyncio.fixture()
#     async def async_client(app, mongo_client):
#         async with LifespanManager(app):           # runs startup/shutdown
#             app.state.client = mongo_client
#             transport = ASGITransport(app=app)
#             async with AsyncClient(transport=transport, base_url="http://test") as client:
#                 yield client
#     ```
#     """

