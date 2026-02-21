from aiogram import BaseMiddleware
from aiogram.types import  Message
from redis.asyncio import Redis
import time


class ThrottlingMiddleware(BaseMiddleware):
    """
    Если юзер спамит — бан на 10 секунд.
    Всё хранится в Redis.
    Без sleep.
    """

    def __init__(self, redis: Redis, rate_limit: float = 1.0, ban_time: int = 10):
        self.redis = redis
        self.rate_limit = rate_limit
        self.ban_time = ban_time

    async def __call__(self, handler, event, data):

        if not isinstance(event, Message):
            return await handler(event, data)

        user = data["event_from_user"]
        user_id = user.id

        now = time.monotonic()

        last_key = f"user:{user_id}:last"
        ban_key = f"user:{user_id}:ban"

        # ---- бан ----
        if await self.redis.exists(ban_key):
            return

        last_time = await self.redis.get(last_key)

        if last_time:
            elapsed = now - float(last_time)

            if elapsed < self.rate_limit:
                # ставим бан
                await self.redis.setex(ban_key, self.ban_time, 1)
                return await event.answer("Вы отправляете сообщения слишком часто!\n" + 
                                          "⛔ Подождите 10 секунд!!!")

        # обновляем время
        await self.redis.set(last_key, now)

        return await handler(event, data)

