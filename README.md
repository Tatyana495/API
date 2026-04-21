# llm-p

Защищённый API для работы с большой языковой моделью через **FastAPI**.

Приложение поддерживает:
- регистрацию и аутентификацию пользователей;
- получение JWT-токена;
- вызов LLM через **OpenRouter**;
- сохранение истории диалога;
- тестирование эндпоинтов через **Swagger UI**.

## Возможности

- регистрация пользователя по email и паролю;
- вход в систему с получением `access_token`;
- доступ к защищённым эндпоинтам по JWT;
- отправка запросов к LLM через OpenRouter;
- сохранение истории сообщений пользователя;
- просмотр истории диалога;
- очистка истории диалога.

## Технологии

- Python
- FastAPI
- Uvicorn
- Pydantic / pydantic-settings
- JWT
- SQLite
- OpenRouter API

## Конфигурация

Настройки читаются из файла `.env`.

Пример:

```env
APP_NAME=llm-p
ENVIRONMENT=local

JWT_SECRET_KEY=change_me_super_secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=app.db

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=stepfun/step-3.5-flash:free
OPENROUTER_REFERER=https://example.com
OPENROUTER_TITLE=llm-fastapi-openrouter
```

## Установка и запуск

### 1. Клонирование проекта

```bash
git clone <repo_url>
cd llm-p
```

### 2. Создание виртуального окружения

```bash
uv venv
```

### 3. Активация окружения

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Установка зависимостей

```bash
uv sync
```

### 5. Запуск приложения

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска будут доступны:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Основные эндпоинты

### Аутентификация

#### `POST /auth/register`
Регистрация пользователя.

Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "Qwerty123!"
}
```

#### `POST /auth/login`
Вход в систему и получение JWT-токена.

Используется форма `application/x-www-form-urlencoded`.

Поля:
- `grant_type=password`
- `username=<email>`
- `password=<пароль>`

Пример ответа:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

#### `GET /auth/me`
Получение данных текущего пользователя.

Требует авторизацию.

---

### Чат

#### `POST /chat`
Отправка запроса в LLM.

Требует авторизацию.

Минимальный пример:

```json
{
  "prompt": "Привет! Напиши короткое приветствие."
}
```

Расширенный пример:

```json
{
  "prompt": "Что ты умеешь? Ответь в 2 предложениях.",
  "system": "Отвечай кратко и понятно.",
  "max_history": 10,
  "temperature": 0.7
}
```

Что происходит при вызове:
1. сервер принимает запрос пользователя;
2. при необходимости добавляет историю в контекст;
3. отправляет запрос во внешний сервис OpenRouter;
4. получает ответ модели;
5. возвращает ответ клиенту;
6. сохраняет диалог в истории.

Пример ответа:

```json
{
  "answer": "Привет! Рад помочь."
}
```

#### `GET /chat/history`
Получение истории диалога пользователя.

Требует авторизацию.

#### `DELETE /chat/history`
Очистка истории диалога пользователя.

Требует авторизацию.

## Как протестировать через Swagger

1. Открой `http://127.0.0.1:8000/docs`
2. Выполни `POST /auth/register`
3. Выполни `POST /auth/login`
4. Нажми **Authorize**
5. Проверь `GET /auth/me`
6. Выполни `POST /chat`
7. Проверь `GET /chat/history`

## Примеры запросов

### Регистрация

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Qwerty123!"}'
```

### Вход

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=user@example.com&password=Qwerty123!"
```

### Запрос к LLM

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Привет! Напиши короткое приветствие."}'
```

## Возможные ошибки

### `409 Conflict`
Пользователь с таким email уже зарегистрирован.

### `401 Unauthorized`
Токен отсутствует, неверен или истёк.

### `422 Validation Error`
Некорректный формат входных данных.

### `502 Bad Gateway`
Ошибка при обращении к OpenRouter.

Возможные причины:
- отсутствует `OPENROUTER_API_KEY`;
- неверный API-ключ;
- приложение не может подключиться к OpenRouter;
- ошибка в конфигурации модели или URL.

## Проверка загрузки конфигурации

При необходимости можно временно вывести в `config.py` диагностическую информацию:

```python
print("OPENROUTER_API_KEY exists:", bool(settings.openrouter_api_key))
print("OPENROUTER_API_KEY len:", len(settings.openrouter_api_key or ""))
print("OPENROUTER_BASE_URL:", settings.openrouter_base_url)
print("OPENROUTER_MODEL:", settings.openrouter_model)
```

## Назначение проекта

Проект демонстрирует реализацию защищённого backend API для интеграции с LLM и может использоваться как учебный пример приложения с:
- JWT-аутентификацией;
- внешней LLM-интеграцией;
- хранением истории запросов;
- документацией через Swagger.