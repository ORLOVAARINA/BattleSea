import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import *
from database.db import check_db
from routers import register_all_routers
import config_data.config as config

# Определяем главную асинхронную функцию main
async def main():
    await check_db()
    bot = Bot(token=token)
    bot_info = await bot.get_me()
    await config.update_data(bot_info)
    dp = Dispatcher()
    register_all_routers(dp)
    await dp.start_polling(bot)

# Проверяем, является ли данный файл точкой входа в приложение
if __name__ == '__main__':
    try:
        logger.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
        print('Exit')

