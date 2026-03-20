from typing import Optional, Dict, Any
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from loguru import logger
import asyncio


class SecurityBotLLMClient:
    """Клиент для взаимодействия с HTTP-сервером LLM (llama.cpp API /completion)"""

    async def __init__(
        self, base_url="http://127.0.0.1", port=8081, timeout=30, n_connects=4
    ):
        self.base_url = base_url.strip()
        self.port = port
        self.timeout = timeout
        self.n_connects = n_connects
        self.session = await self.connect(self)

    async def connect(self) -> ClientSession:
        timeout = ClientTimeout(total=self.timeout)
        async with ClientSession(timeout=timeout) as session:
            connector = TCPConnector(
                limit=self.n_connects, limit_per_host=None
            )  # Увеличиваем лимит соединений

            await connector.connect(
                session, self.base_url.rstrip("/"), port=self.port, ssl=False
            )
        return session

    async def generate(
        self, messages_list: list[Dict[str, str]], temperature: float = 0.7
    ) -> Optional[Dict[str, Any]]:
        """Отправляет запрос к LLM и получает ответ. Возвращает dict или None при ошибке."""

        try:
            payload: Dict[str, Any] = {
                "model": "",
                "messages": messages_list,
                "temperature": temperature,
                "stream": False,
            }

        except Exception as e:
            logger.exception("Ошибка формирования запроса к LLM.")
            return None

        try:
            url = f"http://{self.base_url}:{self.port}/v1/chat/completions"

            response = await self.session.post(url, json=payload)

        except ConnectionRefusedError as e:  # Соединение отвергнуто (сервер недоступен)
            logger.error(f"Соединение отвергнуто (сервер недоступен): {e}")

        try:
            if response.status == 200:
                result = await response.json()
                logger.debug("Успешно получили ответ от сервера")
                return result

            elif response.status in [
                503,
                401,
            ]:  # Ошибки загрузки модели или авторизации
                try:
                    error_text = (
                        await response.text()
                        if hasattr(response, "text")
                        else "Ошибка сервера"
                    )

                    logger.warning(
                        f"Сервер LLM недоступен (код {response.status}): {error_text}"
                    )

                except Exception as e:
                    logger.error(f"Ошибки загрузки модели или авторизации {e}")

            else:  # Остальные ошибки HTTP статуса
                try:
                    if hasattr(response, "text"):
                        error_text = await response.text()

                        logger.error(
                            f"Ошибка сервера HTTP {response.status}: {error_text}"
                        )

                except Exception:  # Ошибка при чтении тела ответа других кодов
                    logger.warning("Ошибка при чтении тела ответа других кодов")
        except asyncio.TimeoutError:  # Таймаут соединения
            logger.warning("Таймаут соединения с локальным LLM.")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
