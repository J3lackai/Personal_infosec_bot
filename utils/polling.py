import asyncio
from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramNetworkError
from loguru import logger


async def safe_start_polling(dp: Dispatcher, bot: Bot):
    while True:
        try:
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logger.warning(f"TelegramNetworkError: {e}, перезапуск через 1 сек.")
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            # если graceful shutdown
            break
        except Exception as e:
            logger.exception(f"Завершение polling-a: {e}")
            await asyncio.sleep(1)
