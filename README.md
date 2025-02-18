Habit Tracker

Habit Tracker – это веб-приложение на Django для отслеживания привычек с использованием Celery и Redis.

Проект поддерживает Docker и CI/CD с GitHub Actions.

 Быстрый запуск (локально)

1 Подготовка
Перед запуском убедитесь, что у вас установлены:

Docker и Docker Compose (установка)
Git

Склонируйте репозиторий:

git clone https://github.com/your-repo/habit-tracker.git
cd habit-tracker
Создайте .env на основе .env.example:

cp .env.example .env
Заполните .env своими данными.

2️ Запуск в Docker
docker-compose up --build

После успешного запуска:

API будет доступно на http://localhost:8000
Nginx – http://localhost
Redis работает в фоне
Для проверки логов:

docker logs -f web
docker logs -f celery
Запуск тестов:

docker exec -it web pytest
Остановка контейнеров:

docker-compose down
Деплой на сервер (Ubuntu 22.04)

1️ Подготовка сервера
Подключитесь к серверу:

ssh your-user@your-server-ip
Установите Docker:

sudo apt update && sudo apt install -y docker.io docker-compose

2️ Развертывание
Скопируйте файлы на сервер:
scp -r .env docker-compose.yaml nginx-docker-setup your-user@your-server-ip:/home/your-user/
Запустите проект:
docker-compose up -d --build
Проверка работы:
docker ps
Обновление после изменений:
docker-compose down && git pull origin main && docker-compose up -d --build
🛠️ CI/CD (GitHub Actions)

Проект автоматически развертывается при пуше в main.

Файл .github/workflows/deploy.yml:

name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Подключение к серверу и обновление контейнеров
        uses: appleboy/ssh-action@v0.1.7
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/${{ secrets.SERVER_USER }}/habit-tracker
            git pull origin main
            docker-compose down
            docker-compose up -d --build
            docker system prune -af

🔑 Добавьте в GitHub Secrets:
SERVER_IP – IP сервера
SERVER_USER – Имя пользователя
SSH_PRIVATE_KEY – SSH-ключ для доступа


Приложение доступно по адресу:
http://your-server-ip

 Используемые технологии

Django REST Framework
Celery + Redis
PostgreSQL
Docker, Docker Compose
Gunicorn + Nginx
GitHub Actions (CI/CD)
