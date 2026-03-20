from llm_client import SecurityBotLLMClient
from loguru import logger
from aiogram.types import Message
import asyncio


async def correct_prompt(message: Message):
    """Обработка ответа от LLM и вывод в диалог"""

    try:
        client = SecurityBotLLMClient(
            base_url="http://127.0.0.1", port=8081
        )  # Укажи IP и порт

        prompt_text = message.text or "Привет"

        messages_list = [
            {
                "role": "system",
                "content": "Ты ИИ-ассистент по компьютерной безопасности. Отвечай кратко и точно.",
            },
            {"role": "user", "content": prompt_text},
        ]
        response_data = await client.generate(messages_list, temperature=0.7)

        if response_data is None:
            return ""

        # Ищем поле content в ответе (основной текст ответа модели)
        completion_content = ""

        if isinstance(response_data, dict):
            try:
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    choice = response_data["choices"][0]

                    # Пытаемся получить content из message
                    if isinstance(choice.get("message"), dict):
                        try:
                            completion_content = str(
                                choice["message"].get("content", "")
                            )

                        except KeyError as e:
                            logger.warning(f"Ключ {e} не найден в choice['message']")

            except Exception as e:
                logger.exception(f"Ошибка парсинга ответа LLM. {e}")
    except asyncio.TimeoutError:
        logger.warning("Таймаут запроса к LLM.")
    finally:
        return completion_content is not None and len(completion_content.strip()) > 0


async def error_prompt():
    pass


async def no_text():
    pass
