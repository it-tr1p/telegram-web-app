#!/usr/bin/env python
# pylint: disable=unused-argument

import json
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens the web app and display chat_id."""
    chat_id = update.effective_chat.id  # Получаем chat_id

    # Отправляем сообщение с кнопкой для открытия WebApp и chat_id
    await update.message.reply_text(
        f"Your chat ID is: <code>{chat_id}</code>"
        "Please press the button below to fill out the form via the WebApp.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open the form!",
                web_app=WebAppInfo(url="https://it-tr1p.github.io/telegram-web-app/?v=3"),
                # Replace with your actual URL
            )
        ),
        parse_mode='HTML'
    )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    data = json.loads(update.effective_message.web_app_data.data)

    # Log the received data
    logger.info(f"Received data from WebApp: {data}")
    print(data['city'])
    await update.message.reply_html(
        text=(
            f"You selected the city: <code>{data['city']}</code><br>"
            f"Number of adults: <code>{data['adults']}</code><br>"
            f"Number of children: <code>{data['children']}</code><br>"
            f"Budget: <code>{data['budget']}</code>"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7429026052:AAHmhRb1MazTFom5JUfx03t9GXT-WuT6_Ic").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
