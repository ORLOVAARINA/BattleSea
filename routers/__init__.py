from aiogram import Dispatcher,F
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import admin_id

# Создаем класс фильтра для проверки прав администратора
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in admin_id:
            return True
        else:
            return False