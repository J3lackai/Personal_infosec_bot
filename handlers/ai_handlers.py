from llm_client import SecurityBotLLMClient
from loguru import logger
from aiogram.types import Message
import asyncio
from aiogram_dialog import DialogManager
from config import LLMServerSettings


async def correct_prompt(message: Message, manager: DialogManager):
    """Обработка ответа от LLM и вывод в диалог"""

    try:
        settings: LLMServerSettings = manager.middleware_data.get("server_settings")
        client = SecurityBotLLMClient(
            base_url=settings.base_url,
            port=settings.port,
            n_connects=settings.n_connects,
            timeout=settings.timeout,
        )  # Достаём из конфига

        prompt_text = message.text

        messages_list = [
            {
                "role": "system",
                "content": settings.sys_prompt,  # sys_prompt из конфига
            },
            {"role": "user", "content": prompt_text},
        ]
        response_data = await client.generate(
            messages_list, temperature=settings.temperature
        )
        if (
            isinstance(response_data, dict)
            and "choices" in response_data
            and len(response_data["choices"]) > 0
        ):
            choice = response_data["choices"][0]

            # Пытаемся получить content из message
            if isinstance(choice.get("message"), dict):
                ai_answer = str(choice["message"].get("content", ""))
                if len(ai_answer.strip()) > 0:
                    message.answer("ИИ Ассистент:\n" + ai_answer)
                    return

        message.answer(settings.ai_busy_msg)

    except KeyError as e:
        logger.warning(f"Ключ {e} не найден в choice['message']")
    except asyncio.TimeoutError:
        logger.warning("Таймаут запроса к LLM.")
    except Exception as e:
        logger.exception(f"Ошибка парсинга ответа LLM. {e}")


async def error_prompt(message: Message):
    message.answer(
        "❌ Ошибка: Длина промпта должна быть больше 0 символов и меньше либо равна 512"
    )


async def no_text(message: Message):
    message.answer(
        "❌ Ошибка: Отправить ИИ-ассистенту можно только текстовое сообщение."
    )
