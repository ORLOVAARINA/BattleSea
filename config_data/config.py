import configparser
from aiogram.types import User
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config = configparser.ConfigParser()
config.read('.env', encoding='utf-8')
data = config['settings']
token = data['token']
admin_id = list(map(int, data['admin_id'].split(',')))

# Создаем класс для хранения данных бота
class BotData:
    def __init__(self):
        self.bot_username = None
        self.bot_name = None

bot_data = BotData() # Создаем экземпляр класса

async def update_bot_data(user: User):
    bot_data.bot_username = user.username
    bot_data.bot_name = user.first_name
    print(f"@{bot_data.bot_username}", bot_data.bot_name)
