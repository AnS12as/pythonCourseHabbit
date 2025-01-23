import requests
import os

from celery import shared_task
from .models import Habit

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, data=data)
    return response.json()


@shared_task
def send_habit_reminders():
    habits = Habit.objects.filter(need_reminder=True)
    for habit in habits:
        if habit.user.profile.telegram_id:
            send_telegram_message(
                chat_id=habit.user.profile.telegram_id,
                message=f"Напоминание о вашей привычке: {habit.action}!",
            )
