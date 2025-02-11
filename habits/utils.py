import os

import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram.

    Аргументы:
        chat_id (str): Telegram ID получателя.
        message (str): Текст сообщения.

    Возвращает:
        dict: Ответ от Telegram API.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, data=data)
    return response.json()
