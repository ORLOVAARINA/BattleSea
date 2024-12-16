import configparser
from aiogram.types import User
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание объекта для работы с конфигурационными файлами
config = configparser.ConfigParser()
config.read('.env', encoding='utf-8')
data = config['settings']
token = data['token']
admin_id = list(map(int, data['admin_id'].split(',')))
weather_api_key = data.get('weather_api_key')

# Создаем класс для хранения данных бота
class BotData:
    def __init__(self):
        self.bot_username = None
        self.bot_name = None

bot_data = BotData() # Создаем экземпляр класса BotData для хранения данных бота

# Асинхронная функция для обновления данных бота
async def update_data(user: User):
    global bot_username
    global bot_name

    bot_username = user.username
    bot_name = user.first_name
    print(f"@{bot_username}", bot_name)