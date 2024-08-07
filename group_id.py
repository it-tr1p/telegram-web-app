from telethon import TelegramClient

# Введите свои данные
api_id = '22799945'
api_hash = 'ed0f03dad816c05929cc330286d12d14'
phone = '+37125974980'

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

client.start(phone=phone,
             password='args-kwargs1-akwa5')


async def get_group_id(link):
    # Получаем информацию о группе по ссылке
    try:
        # Преобразование ссылки в объект чата
        chat = await client.get_entity(link)
        print(f"Group Name: {chat.title}")
        print(f"Group ID: {chat.id}")
    except Exception as e:
        print(f"Ошибка: {e}")


# Запуск функции
with client:
    client.loop.run_until_complete(get_group_id('https://t.me/test_group_for_bot_f'))
