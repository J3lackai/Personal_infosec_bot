from aiogram.types import Message
from loguru import logger
import asyncio
from xposedornot import XposedOrNot
from xposedornot.exceptions import NotFoundError, RateLimitError, APIError

async def correct_email(
    message: Message,
    widget,
    dialog_manager,
    email: str,
) -> None:
    xon = XposedOrNot()
    try:
        result = await asyncio.to_thread(xon.check_email, email)
        logger.info(f"Ищем утечки почты:{email}")
        breach_list = result.breaches[0] if result.breaches else []
        num_breaches=len(breach_list)
        if num_breaches == 0:
            await message.answer("✅ Email не найден ни в одной утечке")
            return
        if num_breaches > 10: #Обрезаем если слишком много результатов
            breaches_text = "\n".join(f"• {breach_list[i]}" for i in range(10))
            breaches_text += "\n... (и другие)\n• " + breach_list[num_breaches-1]
        else: 
            breaches_text = "\n".join(f"• {breach_list[i]}" for i in range(num_breaches))
        await message.answer(
            f"⚠️ Найдено утечек: {num_breaches}\n\n{breaches_text}"
        )
    except NotFoundError:
        await message.answer("✅ Email не найден ни в одной утечке")
    except RateLimitError:
        await asyncio.sleep(1)
        await correct_email(message, widget, dialog_manager, email)
    except APIError as e:
        await message.answer("Сервис в данный момент недоступен 😔\n Попробуйте позже")
        logger.error(f"❌ Ошибка API: {e}")


async def error_email(message: Message, widget, manager, error):
    await message.answer(
        "❌ Ошибка: Введите корректный email. Например: example@gmail.com"
    )

