from loguru import logger
from aiogram.types import Message
from aiogram_dialog import DialogManager
from config import LLMServerSettings
from states import AISG
import openai
from openai import (
    AuthenticationError,
    APIConnectionError,
)


async def correct_prompt(
    message: Message, widget, dialog_manager: DialogManager, value: str
):
    async def server_busy(message: Message, dialog_manager: DialogManager, settings):
        logger.debug("Недостучались к серверу LLM")
        await message.answer(settings.ai_busy_msg)
        await dialog_manager.switch_to(state=AISG.retry_menu)

    """Обработка ответа от LLM и вывод в диалог"""

    try:
        settings: LLMServerSettings = dialog_manager.middleware_data.get(
            "server_settings"
        )
        prompt_text = value

        client = openai.OpenAI(
            timeout=settings.timeout,
            base_url=settings.base_url + ":" + settings.port,
            api_key=settings.psswrd,
            max_retries=0,  # отключаем встроенные ретраи, будем управлять сами
        )

        completion = client.chat.completions.create(
            model="qwen3.5-9b",
            messages=[
                {"role": "system", "content": settings.sys_prompt},
                {"role": "user", "content": prompt_text},
            ],
        )
        logger.debug("Успешно отправили сообщение AI пользователю")
        await message.answer(completion.choices[0].message.content)
        await dialog_manager.switch_to(state=AISG.retry_menu)

    except APIConnectionError:
        logger.error(f"❌ Соединение потеряно: Cannot reach {settings.base_url}")
        await server_busy(message, dialog_manager, settings)
    except AuthenticationError:
        logger.error("❌ Неправиильный ключ API")
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
