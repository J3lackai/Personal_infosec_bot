from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from config import GroqServerSettings, Services


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, server_settings: GroqServerSettings, external_services: Services):
        self.server_settings = server_settings
        self.external_services = external_services

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["server_settings"] = self.server_settings
        data["external_services"] = self.external_services
        return await handler(event, data)
