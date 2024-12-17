import logging
import os
from dotenv import load_dotenv
from aiogram.types import User

# Настройка логирования
logger = logging.getLogger(__name__)  # Используем __name__ для более информативного имени логера
logger.setLevel(logging.DEBUG)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений из переменных окружения. Обработка отсутствующих значений.
token = os.getenv('BOT_TOKEN')
admin_ids_str = os.getenv('ADMIN_IDS')


if not token:
    logger.critical("BOT_TOKEN не найден в .env файле!")
    exit(1)

try:
    admin_id = [int(x) for x in admin_ids_str.split(',')] if admin_ids_str else [] #Обработка случая, если ADMIN_IDS пустой.
except (AttributeError, ValueError):
    logger.error("Неверный формат ADMIN_IDS в .env файле!")
    admin_id = []

# Создаем класс для хранения данных бота
class BotData:
    def __init__(self): # Исправлено: используем __init__
        self.bot_username = None
        self.bot_name = None

bot_data = BotData()  # Создаем экземпляр класса BotData

# Асинхронная функция для обновления данных бота
async def update_data(user: User):
    bot_data.bot_username = user.username  # Обновляем данные через экземпляр класса
    bot_data.bot_name = user.first_name
    logger.info(f"Данные бота обновлены: @{bot_data.bot_username}, {bot_data.bot_name}") # Логируем обновление данных.
