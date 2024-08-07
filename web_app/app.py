from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import os

TOKEN = '7429026052:AAHmhRb1MazTFom5JUfx03t9GXT-WuT6_Ic'
WEBHOOK_URL = 'https://<YOUR_NGROK_URL>/webhook'  # Замените <YOUR_NGROK_URL> на URL вашего ngrok

# Создание экземпляра Flask
app = Flask(__name__)

# Создание бота
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)


# Flask маршрут для получения данных из веб-приложения
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        chat_id = data.get('chat_id', '')
        message = data.get('message', 'No message received')
        if chat_id:
            bot.send_message(chat_id=chat_id, text=message)
    return 'OK'


# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Send me some data.')


# Добавление обработчика команды /start
dispatcher.add_handler(CommandHandler("start", start))


# Запуск бота
def main():
    # Настройка webhook для бота
    bot.set_webhook(url=WEBHOOK_URL)

    # Запуск Flask
    app.run(port=5000)


if __name__ == '__main__':
    main()
