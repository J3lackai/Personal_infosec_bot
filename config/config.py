import os
from dataclasses import dataclass
from dotenv import load_dotenv  # pip install python-dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


@dataclass
class Redis:
    host: str


@dataclass
class Assets:
    file_id1: str
    file_id2: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    log: str
    rate_lim: float


@dataclass
class Config:
    bot: TgBot
    assets: Assets
    redis: Redis


def load_config(path: str | None = None) -> Config:
    if path:
        load_dotenv(dotenv_path=path)

    return Config(
        bot=TgBot(
            token=os.getenv("BOT_TOKEN", ""),
            log=os.getenv("LOG_LEVEL", "INFO"),
            rate_lim=os.getenv("RATE_LIMIT", 1),
            admin_id=int(os.getenv("ADMIN_ID", "1111111111")),
        ),
        assets=Assets(
            file_id1=os.getenv("video_file_id_1", ""),
            file_id2=os.getenv("video_file_id_2", ""),
        ),
        redis=Redis(host=os.getenv("REDIS_HOST", "")),
    )
