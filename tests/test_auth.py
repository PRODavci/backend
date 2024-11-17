import pytest


@pytest.mark.asyncio
async def test_registration(async_client):
    data = {
        "email": "email.test@mail.ru",
        "password": "superstrongpassword",
    }
    # Отправка POST-запроса
    response = await async_client.post("/api/v1/users", json=data)

    # Проверка статуса ответа
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    # Проверка структуры ответа
    response_data = response.json()
    assert "user" in response_data, f"Response body: {response_data}"
    assert "tokens" in response_data, f"Response body: {response_data}"


@pytest.mark.asyncio
async def test_login(async_client):
    data = {
        "email": "email.test@mail.ru",
        "password": "superstrongpassword",
    }

    # Отправка запроса на создание пользователя
    response = await async_client.post("/api/v1/users", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    # Отправка запроса на логин
    response = await async_client.post("/api/v1/users/login", json=data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"

    response_data = response.json()
    assert "user" in response_data, f"Response body: {response_data}"
    assert "tokens" in response_data, f"Response body: {response_data}"

    # Проверка маршрута /me
    token = response_data["tokens"]["access_token"]
    print(token)
    response = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"
