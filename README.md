Сервис аутентификации (спринт 6)


У пользователя может быть несколько ролей (например, подписчик на сериалы от амедиатеки, подписчик на спортивные каналы)
Все роли лежат в таблицу users_roles, связаны с ролями и юзерами.
Админ - пользователь с проставленным флагом is_admin.


## Спринт 7. Добавлено:
1. Аутентификация через google и yandex
2. Rate limit (прописыаается в .env)
3. Jaeger
4. Партиция по типу девайса на таблицу history
5. Токены будут проверяться на других микросервисах - задание с контрактом неактуально
ссылка на проект: https://github.com/fedotovdmitriy14/async_api_movies
Верификация лежит тут fastapi_solution/src/auth:
в ручке /films (fastapi_solution/src/api/v1/films) пример использования



## Запуск:

1. Создать файл с переменными окружения на основе .env.example
2. Запустить docker-compose:

```shell
docker-compose up --build  
```
3. применить миграции:
```shell
docker exec auth_sprint_1_auth_service_1 alembic upgrade head
```

4. Создать суперпользователя (пользователь с флагом is_admin)

```shell
docker exec -it auth_sprint_1_auth_service_1 bash
python3 -m flask create-superuser admin@admin.com admin admin admin
```

список ручек:

auth:

- POST http://127.0.0.1/api/v1/auth/signup - регистрация нового пользователя
- POST http://127.0.0.1/api/v1/auth/login - логин
- POST http://127.0.0.1/api/v1/auth/logout - логаут
- POST://127.0.0.1/api/v1/auth/refresh - получить новую пару токенов

roles (нужны права админа: is_admin = True):

- GET http://127.0.0.1/api/v1/roles/ - получить список все ролей
- POST http://127.0.0.1/api/v1/roles/create - создать роль
- PATCH http://127.0.0.1/api/v1/roles/<role_id> - изменить роль
- DELETE http://127.0.0.1/api/v1/roles/<role_id> - удалить роль

users:

- DELETE http://127.0.0.1/api/v1/users/delete-role - удалить роль у юзера (нужны права админа)
- GET http://127.0.0.1/api/v1/users/login-history - получить историю логинов
- POST http://127.0.0.1/api/v1/users/change-password - изменить пароль
- POST http://127.0.0.1/api/v1/users/change-login - изменить логин
