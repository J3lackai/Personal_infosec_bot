from loguru import logger
from aiogram.types import Message
from aiogram_dialog import DialogManager
from config import GroqServerSettings
from states import AISG
from groq import Groq
from groq import APIConnectionError, AuthenticationError
import re


async def correct_prompt(
    message: Message, widget, dialog_manager: DialogManager, value: str
):
    async def server_busy(message: Message, dialog_manager: DialogManager, settings):
        logger.debug("Недостучались к серверу Groq")
        await message.answer(settings.ai_busy_msg)
        await dialog_manager.switch_to(state=AISG.retry_menu)

    """Обработка ответа от Groq и вывод в диалог"""

    try:
        settings: GroqServerSettings = dialog_manager.middleware_data.get(
            "server_settings"
        )
        prompt_text = value
        client = Groq(api_key=settings.api_key, timeout=settings.timeout)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": settings.sys_prompt},
                {"role": "user", "content": prompt_text},
            ],
            model="qwen/qwen3-32b",
        )
        logger.debug("Успешно отправили сообщение AI пользователю")
        msg = re.sub(
            r"<think>.*?</think>",
            "",
            chat_completion.choices[0].message.content,
            flags=re.DOTALL,
        )
        await message.answer(msg)
        await dialog_manager.switch_to(state=AISG.retry_menu)

    except APIConnectionError:
        logger.error(f"❌ Соединение потеряно: {settings.base_url}")
        await server_busy(message, dialog_manager, settings)
    except AuthenticationError:
        logger.error("❌ Неправильный ключ API")
        await server_busy(message, dialog_manager, settings)
    except TimeoutError:
        logger.error(f"❌ Время истекло: {settings.base_url}")
        await server_busy(message, dialog_manager, settings)
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка сети: {e}")
        await server_busy(message, dialog_manager, settings)


async def error_prompt(message: Message, dialog_manager, widget, error):
    await message.answer(
        "❌ Ошибка: Длина промпта должна быть больше 0 символов и меньше либо равна 512"
    )


async def no_text(message: Message, dialog_manager, error):
    await message.answer(
        "❌ Ошибка: Отправить ИИ-ассистенту можно только текстовое сообщение."
    )
