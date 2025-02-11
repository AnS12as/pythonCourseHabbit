1. Убедитесь, что у вас установлены Docker и Docker Compose.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/AnS12as/pythonCourseHabbit.git
   cd pythonCourseHabbit
   

Развертывание на сервере

1. **Настроить сервер**  
   - Установить `Docker`, `Docker Compose`, `Git`
   - Открыть SSH (`sudo ufw allow OpenSSH`)
   - Открыть порты (`sudo ufw allow 80/tcp` и `443/tcp`)

2. **Склонировать проект**  
   ```bash
   git clone git@github.com:username/habit_tracker.git
   cd habit_tracker