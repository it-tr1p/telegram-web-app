from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Ваш токен бота
TOKEN = '7429026052:AAHmhRb1MazTFom5JUfx03t9GXT-WuT6_Ic'

# Создание экземпляра Flask
app = Flask(__name__)

# Создание бота
bot = Bot(token=TOKEN)


# Flask маршрут для получения данных из веб-приложения
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        chat_id = data.get('chat_id', '')
        message = data.get('message', 'No message received')
        if chat_id:
            bot.send_message(chat_id=chat_id, text=message)
    return jsonify(success=True)


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me some data.')


# Запуск long-polling
async def main():
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчика команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск Flask в отдельном потоке
    from threading import Thread
    Thread(target=lambda: app.run(port=5000)).start()

    # Запуск long-polling
    await application.start_polling()
    await application.idle()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
