#!/bin/sh

# Ожидание запуска БД
echo "Ожидание запуска базы данных..."
/app/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "База данных доступна!"

# Выполняем миграции
echo "Выполняем миграции..."
python manage.py migrate

# Собираем статику
echo "Собираем статику..."
python manage.py collectstatic --noinput

# Запуск Gunicorn
echo "Запускаем Gunicorn..."
exec gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000
