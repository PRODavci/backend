## Запуск докера

```shell
docker build . --tag fastapi-boilerplate

docker run -p 8000:8000 fastapi-boilerplate
```

```shell
docker compose up --build
```

## Тестирование

```shell
pytest tests --cov
```
