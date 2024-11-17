import pytest


@pytest.mark.asyncio
async def test_registration(async_client):
    data = {
        "email": "email.test@mail.ru",
        "password": "superstrongpassword",
    }
    response = await async_client.post("/api/v1/users", json=data)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    response_data = response.json()
    assert "user" in response_data, f"Response body: {response_data}"
    assert "tokens" in response_data, f"Response body: {response_data}"


@pytest.mark.asyncio
async def test_login(async_client):
    data = {
        "email": "email.test@mail.ru",
        "password": "superstrongpassword",
    }

    response = await async_client.post("/api/v1/users", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    response = await async_client.post("/api/v1/users/login", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    response_data = response.json()
    assert "user" in response_data, f"Response body: {response_data}"
    assert "tokens" in response_data, f"Response body: {response_data}"

    token = response_data["tokens"]["access_token"]

    response = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"


async def test_change_password(async_client):
    data = {
        "email": "email.test@mail.ru",
        "password": "superstrongpassword",
    }

    response = await async_client.post("/api/v1/users", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    token = response.json()["tokens"]["access_token"]

    response = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    data = {
        "old_password": "superstrongpassword",
        "new_password": "notsuperstrongpassword",
    }

    response = await async_client.post(
        "/api/v1/users/change_password", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    response = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}, body: {response.text}"

    data = {
        "email": "email.test@mail.ru",
        "password": "notsuperstrongpassword",
    }

    response = await async_client.post("/api/v1/users/login", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    token = response.json()["tokens"]["access_token"]

    response = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"
