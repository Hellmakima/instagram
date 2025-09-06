import pytest
from httpx import AsyncClient


# assuming we have fixtures `async_client`, `user_repo` and already tested.
# This is kinda integration test, coz we are testing the function as well as the DB.
# @pytest.mark.asyncio
# async def test_register_happy_path(async_client: AsyncClient, user_repo):
#     payload = {
#         "username": "testuser",
#         "email": "test@example.com",
#         "password": "StrongPass123!"
#     }

#     resp = await async_client.post("/register", json=payload)

#     # API response check
#     assert resp.status_code == 201
#     data = resp.json()
#     assert data["message"] == "User registered successfully. Please proceed to login."

#     # DB check
#     user = await user_repo.find_by_username("testuser")
#     assert user is not None
#     assert user["email"] == "test@example.com"
#     assert user["is_verified"] is False


# this is a function test, only testing the function, not the DB.
@pytest.mark.asyncio
async def test_register_happy_path_function(async_client: AsyncClient):
    csrf_resp = await async_client.get("/auth/csrf-token")
    print(csrf_resp.json())
    csrf_token = csrf_resp.json()["data"]["csrf_token"]

    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass123!"
    }

    resp = await async_client.post(
        "/auth/register",
        json=payload,
        headers={"X-CSRF-Token": csrf_token}
    )

    # API response check
    print(resp.json())
    assert resp.status_code == 201
    data = resp.json()
    assert data["message"] == "User registered successfully. Please proceed to login."
