from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Callable, Dict, Awaitable
from loguru import logger
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError


class IfBotBlockedMiddleware(BaseMiddleware):
    """Мидлварь для отслеживания не заблочил ли юзер бота."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except TelegramForbiddenError as e:
            if "bot was blocked by the user" in str(e).lower():
                user_id = getattr(event.from_user, "id", "unknown")
                logger.info(f"Пользователь {user_id} заблокировал бота.")
        except TelegramBadRequest as e:
            # например: "Chat not found"
            logger.warning(f"BadRequest: {e}")
            return
