import os

import telegram
from celery import shared_task

from .models import Habit

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        telegram_id = user.profile.telegram_id
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

        message = f"Reminder: {habit.action} at {habit.time} in {habit.place}."
        bot.send_message(chat_id=telegram_id, text=message)
    except Exception as e:
        print(f"Error sending reminder: {e}")
