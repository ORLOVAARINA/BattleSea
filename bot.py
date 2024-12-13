from aiogram import Bot, Dispatcher
from config_data.config import *  # Импортируем bot_data
from database.db import check_db
from filters import register_all_routers
import asyncio

import config_data.config as conf

async def main():
    await check_db()
    bot = Bot(token=token)
    await bot.delete_webhook()
    bot_info = await bot.get_me()
    await update_bot_data(bot_info) # Используем функцию update_bot_data
    dp = Dispatcher()
    register_all_routers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
        print('Exit')

