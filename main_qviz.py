from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, \
    ConversationHandler, filters

# Глобальные переменные для хранения ответов пользователя
answers = {}

# Константы для состояний диалога
SELECT_CITY, SELECT_ADULTS, SELECT_CHILDREN, ENTER_BUDGET = range(4)

# Словарь для хранения пользователей в зависимости от города
users = {
    'Пхукет': {'tg_user_name': 'user_phuket', 'tg_user_id': 6861602355},
    'Паттайя': {'tg_user_name': 'user_pattaya', 'tg_user_id': 6861602355}
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я помогу тебе с выбором тура. Давай начнем с небольшого опроса.\n\n"
        "Выберите город:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Пхукет", callback_data='city_Пхукет'),
             InlineKeyboardButton("Паттайя", callback_data='city_Паттайя')]
        ])
    )
    return SELECT_CITY


async def select_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    city = query.data.split('_')[1]
    answers['city'] = city

    await query.edit_message_text(
        text=f"Вы выбрали город: {city}\n\n"
             "Выберите количество взрослых:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1-2", callback_data='adults_1-2'),
             InlineKeyboardButton("3-5", callback_data='adults_3-5'),
             InlineKeyboardButton("6-8", callback_data='adults_6-8'),
             InlineKeyboardButton("10+", callback_data='adults_10+')]
        ])
    )
    return SELECT_ADULTS


async def select_adults(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    adults = query.data.split('_')[1]
    answers['adults'] = adults

    await query.edit_message_text(
        text=f"Вы выбрали количество взрослых: {adults}\n\n"
             "Выберите количество детей:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1", callback_data='children_1'),
             InlineKeyboardButton("2", callback_data='children_2'),
             InlineKeyboardButton("3", callback_data='children_3'),
             InlineKeyboardButton("4", callback_data='children_4'),
             InlineKeyboardButton("5", callback_data='children_5')]
        ])
    )
    return SELECT_CHILDREN


async def select_children(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    children = query.data.split('_')[1]
    answers['children'] = children

    await query.edit_message_text(
        text=f"Вы выбрали количество детей: {children}\n\n"
             "Напишите ваш бюджет в долларах, например, 1000:"
    )
    return ENTER_BUDGET


async def enter_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    budget = update.message.text
    answers['budget'] = budget

    # Отправляем сообщение о завершении опроса
    await update.message.reply_text(
        "Спасибо, ваша заявка передана владельцу, скоро с вами свяжутся, хорошего дня!"
    )

    # Отправляем ответы владельцу в зависимости от выбранного города
    city = answers['city']
    owner_id = users[city]['tg_user_id']

    await context.bot.send_message(
        chat_id=owner_id,
        text=f"Новая заявка от пользователя @{update.message.from_user.username}:\n"
             f"Город: {answers['city']}\n"
             f"Количество взрослых: {answers['adults']}\n"
             f"Количество детей: {answers['children']}\n"
             f"Бюджет: {answers['budget']}"
    )

    return ConversationHandler.END


def main():
    application = Application.builder().token("7427957219:AAELVhkVlZSYLBc_d8t7Crx4za5j8En1Si8").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_CITY: [CallbackQueryHandler(select_city)],
            SELECT_ADULTS: [CallbackQueryHandler(select_adults)],
            SELECT_CHILDREN: [CallbackQueryHandler(select_children)],
            ENTER_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_budget)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
