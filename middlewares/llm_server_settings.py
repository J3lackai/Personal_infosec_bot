from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from config import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, server_settings: Config):
        self.server_settings = server_settings

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["server_settings"] = self.server_settings
        return await handler(event, data)
