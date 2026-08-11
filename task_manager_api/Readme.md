# Task Manager API

REST API для управления задачами с аутентификацией пользователей.

 Стек

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- JWT (OAuth2PasswordBearer)
- Pydantic (BaseModel)

Функциональность

- Регистрация и авторизация пользователей (JWT)
- Каждый пользователь видит только свои задачи
- CRUD операции над задачами:
  - GET /tasks — получить список задач
  - POST /tasks — создать задачу
  - PUT /tasks/{id} — обновить задачу
  - DELETE /tasks/{id} — удалить задачу

 Запуск локально

1. Клонировать репозиторий
2. Создать файл .env по образцу .env.example
3. Установить зависимости:
   
    pip install -r requirements.txt
    
4. Применить миграции:
   
    alembic upgrade head
    
5. Запустить сервер:
   
    uvicorn main:app --reload
    
SWAGGER UI

После запуска доступно по адресу: http://localhost:8000/docs
