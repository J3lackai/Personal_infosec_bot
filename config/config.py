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
    log: str
    rate_lim: float

@dataclass
class Services:
    virus_total_key: str
@dataclass
class GroqServerSettings:
    timeout: float
    api_key: str
    sys_prompt: str
    temperature: float
    ai_busy_msg: str


@dataclass
class Config:
    bot: TgBot
    redis: Redis
    external_services: Services
    groq_server: GroqServerSettings


def load_config(path: str | None = None) -> Config:
    if path:
        load_dotenv(dotenv_path=path)

    return Config(
        bot=TgBot(
            token=os.getenv("BOT_TOKEN", ""),
            log=os.getenv("LOG_LEVEL", "INFO"),
            rate_lim=os.getenv("RATE_LIMIT", 1),
        ),
        external_services=Services(
            virus_total_key = os.getenv("VIRUSTOTAL_API_KEY")
        ),
        redis=Redis(host=os.getenv("REDIS_HOST", "")),
        groq_server=GroqServerSettings(
            timeout=float(os.getenv("LLM_TIMEOUT", 30)),
            sys_prompt=os.getenv(
                "SYS_PROMPT",
                "Ты ИИ-ассистент по компьютерной безопасности. Отвечай кратко и точно. "
                "Если вопрос общий и не связан с математикой, программированием и кибербезопасностью, "
                "сообщи пользователю что ты ИИ-ассистент по личной информационной безопасности.",
            ),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
            ai_busy_msg=os.getenv(
                "AI_BUSY_MSG",
                "ИИ ассистент сейчас недоступен 🙁\nПопробуйте обратиться к нему позже.",
            ),
        ),
    )
