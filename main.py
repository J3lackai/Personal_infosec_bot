import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio import Redis
from loguru import logger
from utils import safe_start_polling
from config import Config, load_config
from middlewares import ThrottlingMiddleware, IfBotBlockedMiddleware, ConfigMiddleware
from handlers import router as usr_router
from aiogram_dialog import setup_dialogs
from dialogs import start_dialog, tool_dialog, guide_dialog, ai_dialog, contact_dialog


async def main() -> None:
    config: Config = load_config()
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    redis = Redis(host=config.redis.host)

    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True,
            prefix="fsm",
        ),
    )

    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )
    logger.debug("Init bot/redis/storage/dp")

    # middlewares
    dp.message.outer_middleware(
        IfBotBlockedMiddleware()
    )  # Не обрабатываем апдейты если бот в блоке
    dp.message.outer_middleware(ThrottlingMiddleware(redis=redis))  # Защита от спама
    dp.update.middleware(ConfigMiddleware(config.groq_server, config.external_services))
    # filters
    # dialogs
    usr_router.include_router(contact_dialog)
    usr_router.include_router(start_dialog)
    usr_router.include_router(tool_dialog)
    usr_router.include_router(guide_dialog)
    usr_router.include_router(ai_dialog)

    # routers

    dp.include_router(usr_router)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        logger.info("Bot started")
        await safe_start_polling(dp, bot)
    finally:
        await redis.aclose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
