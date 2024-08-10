from flask import Flask, request, jsonify
from telegram import Bot

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

if __name__ == '__main__':
    app.run(port=5000)
