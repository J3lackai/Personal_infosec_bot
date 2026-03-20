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
class LLMServerSettings:
    timeout: float
    n_connects: int
    sys_prompt: str
    base_url: str
    port: str
    temperature: float
    ai_busy_msg: str


@dataclass
class Config:
    bot: TgBot
    assets: Assets
    redis: Redis
    llm_server: LLMServerSettings


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
        llm_server=LLMServerSettings(
            timeout=float(os.getenv("LLM_TIMEOUT", 30)),
            sys_prompt=os.getenv(
                "SYS_PROMPT",
                "Ты ИИ-ассистент по компьютерной безопасности. Отвечай кратко и точно.",
            ),
            port=os.getenv("LLM_PORT", 8081),
            base_url=os.getenv("LLM_BASE_URL", "http://192.168.31.16"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
            ai_busy_msg=os.getenv(
                "AI_BUSY_MSG",
                "ИИ ассистент сейчас недоступен 🙁\nПопробуйте обратиться к нему позже.",
            ),
        ),
    )
