from aiogram import Bot, Dispatcher
from config_data.config import *
from database.db import check_db
from filters import register_all_routers
import asyncio

import test as test
import config_data.config as config


async def main():
    await check_db()
    bot = Bot(token=token)
    await bot.delete_webhook()
    bot_info = await bot.get_me()
    await config.update_data(bot_info)
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