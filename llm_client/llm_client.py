import asyncio
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from loguru import logger
import json


class SecurityBotLLMClient:
    """Клиент для взаимодействия с HTTP-сервером LLM"""

    def __init__(self, base_url="http://127.0.0.1", port=8081):
        self.base_url = base_url.strip()
        self.port = port

    async def generate(self, prompt: str):
        """Отправляет запрос к LLM и получает ответ"""

        timeout = ClientTimeout(total=30.0)  # Таймаут 30 секунд

        payload = {
            "model": "",  # Если у тебя нет параметра model в URL — оставь пустым или задай ID модели вручную
            "messages": [
                {
                    "role": "system",
                    "content": "Ты ИИ-ассистент по компьютерной безопасности. Отвечай кратко и точно.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "stream": False,  # Если сервер поддерживает потоковую передачу — поставь True для экономии времени ответа
        }

        try:
            async with ClientSession(timeout=timeout) as session:
                connector = TCPConnector(limit=10)
                await connector.connect(
                    session, self.base_url, port=self.port, ssl=False
                )

                payload_json = f'{{"model": "", "messages": [{", ".join(f"{k}: {v}" for k, v in json.dumps(payload).split(",")[:-1])}, {"role": "user", "content": "{prompt}"}]}}'.replace(
                    " ", ""
                )  # Упрощённая JSON структура
                async with session.post(
                    f"http://{self.base_url}:{self.port}/generate",
                    data=json.dumps(payload),
                    content_type="application/json",
                ) as response:
                    if response.status == 200:
                        return await response.json()  # Получаем ответ LLM

                    else:
                        raise Exception(
                            f"Ошибка сервера {response.status}: {await response.text()}"
                        )

        except asyncio.TimeoutError:
            logger.error("Таймаут соединения с локальным LLM.")

        except ConnectionRefusedError as e:
            logger.warning(f"Соединение отвергнуто (сервер недоступен): {e}")

        except Exception as e:  # Обработка остальных ошибок
            logger.exception(f"Неожиданная ошибка при запросе к LLM:{e}")
