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

Запуск проекта

Перед создание проекта необходимо установить свой данные для правильного запуска докер контейнеров а именно : какая база данных будет использоваться, пользователя бд, пароль, хост, порт, секретный ключ проекта.

infra/.env <--- в этот файл
Необходимо перейти в папку с файлом
infra/docker-compose.yaml
Создание образа проекта выполняем команды в терминале с docker-compose.yaml
docker-compose build 
Проводим миграции, создаём superuser, собираем статику
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
Загрузка базы данных fixtures.json:
python3 manage.py shell
в консоли:

from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
Выход из консоли

quit()
python manage.py loaddata dump.json
Запускаем проект
docker-compose up 
Остановка проекта
docker-compose down 

Разработчик:
 Слизская Лариса