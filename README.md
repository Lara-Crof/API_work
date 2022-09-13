Проект сервиса API для YaMDB - социальной сети, которая собирает отзывы (Review) и оценки пользователей на произведения (Title) в разных категориях и жанрах, а так же комментарии к отзывам. Произведения делятся на категории (Category) и жанры (Genres), список которых может быть расширен, но правами на добавление новых жанров, категорий и произведений обладает только администратор. Для авторизации пользователей используется код подтверждения.Для аутентификации пользователей используются JWT-токены.

Реализован REST API CRUD для моделей проекта, для аутентификации примненяется JWT-токен. В проекте реализованы пермишены, фильтрации, сортировки и поиск по запросам клиентов, реализована пагинация ответов от API, установлено ограничение количества запросов к API. 

Системные требования
Python 3.7+
Works on Linux, Windows, macOS
Стек технологий:
Python 3.8
Django 3.2
Django Rest Framework
Simple-JWT
Nginx
Gunicorn
GitHub Actions (CI/CD)