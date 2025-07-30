# Django Wallets Operations API

**Django Wallets Operations API** — это RESTful веб-приложение для управления кошельками и финансовыми операциями (пополнение и снятие средств) с поддержкой:
- JWT-аутентификации (через `djangorestframework-simplejwt`);
- регистрации и входа пользователей;
- нескольких пользователей на один кошелёк;
- истории операций;
- конкурентных операций;
- автодокументации через `drf-spectacular` (Swagger UI / ReDoc).

---

## Технологии

- Python 3.11+
- Django 5
- Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- drf-spectacular (OpenAPI docs)
- Pytest + coverage

---

## Основные приложения

```
.
├── users/        # Регистрация и аутентификация пользователей
├── wallets/      # Логика кошельков и операций
├── app/          # Настройки Django-проекта

```

---

## Как запустить проект

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Putopu3m/Django-wallets-operations.git
cd Django-wallets-operations
```

### 2. Соберите и запустите контейнеры

```bash
docker-compose up --build
```

### 3. Создание суперпользователя (в другом терминале):

```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## Эндпоинты авторизации (JWT)

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/auth/register/` | Регистрация нового пользователя |
| `POST` | `/auth/token/` | Получение access и refresh токена |
| `POST` | `/auth/token/refresh/` | Обновление access токена |

---

## Эндпоинты API (кошельки)

| Метод | URL | Описание |
|-------|-----|----------|
| `GET/POST` | `/api/v1/wallets/` | Список и создание кошельков |
| `GET` | `/api/v1/wallets/<id>/` | Получение одного кошелька |
| `POST` | `/api/v1/wallets/<id>/operation/` | Проведение операции (`operation_type`: deposit/withdraw, `amount`) |
| `GET` | `/api/v1/wallets/operations/` | Список всех операций пользователя |

Все запросы требуют **авторизации по JWT** (`Authorization: Bearer <token>`)

---

## Документация API

После запуска проекта доступны:

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`
- OpenAPI schema (json): `/api/schema/`



## Тестирование

Для запуска тестов и покрытия:

```bash
docker-compose exec backend pytest --cov
```

---