import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError
from config_data.config import token, logger
from database.db import check_db
from handlers import user_handlers, admin_handlers
from routers import IsAdmin

import config_data.config as config


async def main():
    await check_db()
    bot = Bot(token=token)
    try:
      bot_info = await bot.get_me()
      await config.update_data(bot_info)
      dp = Dispatcher()

      # Фильтрация роутеров (не импортируется, поэтому используется здесь)
      admin_handlers.router.message.filter(F.chat.type == "private", IsAdmin())
      user_handlers.router.message.filter(F.chat.type == "private")
      dp.include_router(admin_handlers.router)  # Админ роутер
      dp.include_router(user_handlers.router)  # Юзер роутер


      await dp.start_polling(bot)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
         await bot.session.close()

if __name__ == '__main__':
    try:
        logger.info("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
        print('Exit')