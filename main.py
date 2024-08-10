import csv
import logging
import os

from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerChannel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

api_id = '22799945'
api_hash = 'ed0f03dad816c05929cc330286d12d14'
phone = '+37125974980'
SEND_MESSAGE = False
message_for_client = ('Здравствуйте, увидели ваше сообщение об аренде, '
                      'пройдите короткий опрос в нашем боте, '
                      'и после уточнения информации о заселении с вами в '
                      'течение 30 минут свяжется собственник.\nhttps://t.me/test_adf_add_bot')

# Ключевые слова для поиска
keywords = ['сниму', 'ищу', 'интересует', 'квартира', 'вилла', 'кондо', 'ищем',
             'title', 'дом', 'снимем', 'арендую', 'арендуем', 'предложите', 'квартиру', 'аппартаментов',
            'аппартаменты', 'аренды', 'нужна', 'нужны', 'снять']

ban_keywords = ['сдам', 'сдается', 'свободны', 'свободна', 'доступна', 'пересдадим', 'пересдам', 'EnjoyCarRent', 'авто',
                'мастер', 'smm', 'акция',
                'toyota', 'nissan', 'mazda', 'honda', 'mitsubish', 'ford', 'mg',
                'сервис', 'продам', 'недвижимость', 'продаю',
                '@valerypodolyak']

k = 'свободна'
client = TelegramClient('session_name', api_id, api_hash)


async def read_group_links(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file]
    return links


async def get_group_ids(links):
    group_ids = []
    for link in links:
        try:
            chat = await client.get_entity(link)
            if isinstance(chat, PeerChannel):
                group_ids.append(chat.id)
        except Exception as e:
            logger.error(f"Ошибка при получении группы {link}: {e}")
    return group_ids


@client.on(events.NewMessage)
async def handle_new_message(event):
    message = event.message.message
    sender = await event.get_sender()

    if sender.bot:
        return

    message_lower = message.lower()

    # Проверка наличия ключевых слов
    if any(keyword in message_lower for keyword in keywords):
        # Проверка отсутствия запрещенных ключевых слов
        if not any(ban_keyword in message_lower for ban_keyword in ban_keywords):
            chat = await event.get_chat()
            chat_username = chat.username if chat.username else 'c/' + str(abs(chat.id))
            user_info = {
                'tg_id': sender.id,
                'tg_user_name': sender.username,
                'group_link': f"https://t.me/{chat_username}",
                'message_link': f"https://t.me/{chat_username}/{event.message.id}",
                'text_message': message
            }
            logger.info(f"Новое сообщение от пользователя @{sender.username}: {message}")
            save_to_csv(user_info)
            if SEND_MESSAGE:
                await client.send_message(sender.id, message_for_client)


def save_to_csv(user_info):
    file_exists = os.path.isfile('user_messages.csv')
    with open('user_messages.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['tg_id', 'tg_user_name', 'group_link', 'message_link', 'text_message'])

        if not file_exists:
            writer.writeheader()

        writer.writerow(user_info)


async def main():
    await client.start(phone=phone, password='args-kwargs1-akwa5')

    # Чтение ссылок из файла
    group_links = await read_group_links('group_links.txt')

    # Получение ID групп
    group_ids = await get_group_ids(group_links)

    # Подписка на группы
    for group_id in group_ids:
        await client(JoinChannelRequest(group_id))

    logger.info("Бот запущен и мониторит сообщения...")

    # Не останавливать бота
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
