import secrets
import string
import re
import vt
from config import Services
from typing import Dict, Any
from urllib.parse import urlparse
import requests
from aiogram_dialog.widgets.kbd import ManagedMultiselect
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from datetime import datetime
from loguru import logger
from states import ToolSG
import asyncio
from lexicon import vt_error_mssgs, vt_fallback_e_msg
# Коды ошибок VirusTotal API → человекочитаемые сообщения

async def generate_password(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
) -> str:
    """Генерирует надёжный пароль по выбранным параметрам"""

    list_prop = dialog_manager.dialog_data.get("list_checked_prop", [])
    list_case = dialog_manager.dialog_data.get("list_checked_case", [])
    len_psswrd = int(dialog_manager.dialog_data.get("len_psswrd", 12))

    chars = ""

    # Латиница
    if "3" in list_prop:
        if "1" in list_case:
            chars += string.ascii_lowercase

        if "2" in list_case:
            chars += string.ascii_uppercase

    # Цифры
    if "1" in list_prop:
        chars += string.digits

    # Спецсимволы
    if "2" in list_prop:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Кириллица
    if "4" in list_prop:
        lower_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        upper_ru = lower_ru.upper()

        if "1" in list_case:
            chars += lower_ru

        if "2" in list_case:
            chars += upper_ru

    # Если пользователь ничего не выбрал
    if not chars:
        chars = string.ascii_letters + string.digits

    password = "".join(secrets.choice(chars) for _ in range(len_psswrd))
    dialog_manager.switch_to(state=ToolSG.menu)
    await callback.message.answer(password)

async def set_default_multiselect(    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager):

    multiselect = dialog_manager.find("high_lower_case")
    await multiselect.set_checked("1", True)
    await multiselect.set_checked("2", True)

    multiselect = dialog_manager.find("pswrd_prop")
    await multiselect.set_checked("1", True)
    await multiselect.set_checked("2", True)
    await multiselect.set_checked("3", True)
    await multiselect.set_checked("4", True)

async def multiselect_clicked_prop(
    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager,
    value: str,

):
    dialog_manager.dialog_data.update(list_checked_prop=multiselect.get_checked())


async def multiselect_clicked_case(
    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data.update(list_checked_case=multiselect.get_checked())


async def correct_len_handler(
    message: Message, widget, manager: DialogManager, value: int
):
    manager.dialog_data["len_psswrd"] = value
    await manager.next()


async def error_len_handler(message: Message, widget, manager, error):
    await message.answer("❌ Введите только число\nПример: 12")

async def error_len_handler(message: Message, widget, manager, error):
    await message.answer("❌ Введите только число\nПример: 12")

async def error_link(message: Message, widget, manager, error):
    await message.answer("❌ Введите корректную ссылку\nПример: https://example.com")

async def check_password_strength(
    message: Message,
    widget,
    manager: DialogManager,
    value: int,
):
    """Анализирует пароль и отправляет результат пользователю."""

    tips = []
    score = 0
    psswrd = (message.text).strip()
    logger.info(psswrd)

    # Длина
    length = len(psswrd)
    if length < 12:
        score += 1
        tips.append("⚠️ Рекомендуется от 12 символов")
    elif length < 16:
        score += 2
    else:
        score += 3

    # Регистр
    has_upper = bool(re.search(r"[A-Z]", psswrd))
    has_lower = bool(re.search(r"[a-z]", psswrd))
    if has_upper and has_lower:
        score += 2
    elif has_upper or has_lower:
        score += 1
        tips.append("⚠️ Используйте буквы обоих регистров")
    else:
        tips.append("❌ Нет букв")

    # Цифры
    if re.search(r"\d", psswrd):
        score += 1
    else:
        tips.append("❌ Нет цифр")

    # Спецсимволы
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", psswrd):
        score += 2
    else:
        tips.append("❌ Нет спецсимволов (!@#$%^&* и др.)")

    # Повторы
    if re.search(r"(.)\1{2,}", psswrd):
        score -= 1
        tips.append("⚠️ Есть повторяющиеся символы (aaa, 111...)")

    # Частые паттерны
    common_sequences = ["123456", "qwerty", "abcdef", "111111", "password", "qweasd"]
    if any(seq in psswrd.lower() for seq in common_sequences):
        score -= 2
        tips.append("❌ Содержит очевидную последовательность")

    # Только цифры
    if re.fullmatch(r"\d+", psswrd):
        score -= 1
        tips.append("❌ Пароль состоит только из цифр")

    score = max(0, score)

    # Уровень
    if score <= 2:
        level = "🔴 Очень слабый"
    elif score <= 4:
        level = "🟠 Слабый"
    elif score <= 6:
        level = "🟡 Средний"
    elif score <= 7:
        level = "🟢 Сильный"
    else:
        level = "💪 Очень сильный"

    # 👇 ОТПРАВКА РЕЗУЛЬТАТА
    text = (
        f"🔐 Пароль: `{psswrd}`\n"
        f"📊 Уровень: {level}\n"
        f"⭐ Оценка: {score}/10\n\n"
    )

    if tips:
        text += "💡 Рекомендации:\n" + "\n".join(tips)
    await message.answer(text)



def leaks_email(email: str, widget, dialog_manager) -> Dict[str, Any]:
    """Проверяет email на утечки через HaveIBeenPwned API."""
    clean_email = email.lower().strip()
    result = {"email": clean_email, "has_leaks": False, "leaks": []}

    try:
        response = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{clean_email}",
            headers={"hibp-api-key": "YOUR_API_KEY", "user-agent": "SecurityBot"},
            timeout=10,
        )
        if response.status_code == 200:
            breaches = response.json()
            result["has_leaks"] = len(breaches) > 0
            result["leaks"] = [
                {
                    "name": breach.get("Name", ""),
                    "date": breach.get("BreachDate", ""),
                    "data_classes": breach.get("DataClasses", []),
                }
                for breach in breaches
            ]
        elif response.status_code == 404:
            result["has_leaks"] = False
    except requests.RequestException as e:
        logger.error(f"Ошибка HaveIBeenPwned API: {e}")

    return result


async def correct_link(
    message: Message,
    widget,
    dialog_manager,
    url: str,
) -> None:
    """Проверяет ссылку с помощью сервиса Virus Total и возвращает результат"""
    services = dialog_manager.middleware_data.get("external_services")
    api_key: str = services.virus_total_key

    async with vt.Client(apikey=api_key) as client:
        # 1. Сканируем URL и ждём завершения анализа
        try:
            analysis: vt.Object = await client.scan_url_async(
                url, wait_for_completion=True
            )
        except vt.APIError as e:
            logger.error(
                "VirusTotal APIError on scan_url | code={} message={} url={}",
                e.code, str(e), url,
            )
            user_msg = vt_error_mssgs.get(e.code, vt_fallback_e_msg)
            await message.answer(user_msg)
            return
        except asyncio.TimeoutError:
            logger.error("VirusTotal timeout on scan_url | url={}", url)
            await message.answer("Сервис проверки не ответил вовремя. Попробуйте позже ⌛")
            return
        except Exception as e:
            logger.exception("Unexpected error on scan_url | url={} error={}", url, e)
            await message.answer(vt_fallback_e_msg)
            return

        # 2. Читаем stats прямо из объекта анализа
        try:
            stats: dict = analysis.stats  # атрибут vt.Object
        except AttributeError:
            # Если анализ ещё не содержит stats — пробуем через get()
            stats = analysis.get("stats") or {}

        if not stats:
            logger.warning(
                "VirusTotal: empty stats in analysis | url={} analysis_id={}",
                url, analysis.id,
            )
            await message.answer("Не удалось получить результаты анализа. Попробуйте позже 🤔")
            return

        malicious: int = stats.get("malicious", 0)
        suspicious: int = stats.get("suspicious", 0)
        harmless: int = stats.get("harmless", 0)
        undetected: int = stats.get("undetected", 0)

        logger.info(
            "VirusTotal result | url={} malicious={} suspicious={} harmless={} undetected={}",
            url, malicious, suspicious, harmless, undetected,
        )

    # 3. Формируем ответ пользователю
    if malicious == 0 and suspicious == 0:
        text = "✅ Ссылка безопасна"
    else:
        parts = []
        if malicious:
            parts.append(f"угроз: {malicious}")
        if suspicious:
            parts.append(f"подозрительных: {suspicious}")
        text = "⚠️ Ссылка опасна: " + ", ".join(parts)

    await message.answer(text)


def analysis_site(url: str) -> Dict[str, Any]:
    """
    Комплексная проверка сайта: WHOIS, SSL-сертификат, HTTP-заголовки.
    Возвращает словарь с результатами каждой проверки и общим вердиктом.
    """
    result = {
        "url": url,
        "whois": None,
        "ssl": None,
        "headers": None,
        "is_safe": False,
        "message": "",
    }

    # ---------- 2. SSL (SSL Labs) ----------
    parsed = urlparse(url)
    hostname = parsed.hostname or url
    ssl_result = {
        "grade": "F",
        "valid_ssl": False,
        "issuer": "",
        "expiry_date": "",
        "days_until_expiry": 0,
        "issues": [],
    }
    try:
        resp = requests.get(
            f"https://api.ssllabs.com/api/v3/analyze?host={hostname}", timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            endpoints = data.get("endpoints", [])
            if endpoints:
                endpoint = endpoints[0]
                ssl_result["grade"] = endpoint.get("grade", "F")
                ssl_result["valid_ssl"] = ssl_result["grade"] not in ["F", "T"]

                cert_info = endpoint.get("details", {}).get("cert", {})
                ssl_result["issuer"] = cert_info.get("issuerSubject", "")

                not_after = cert_info.get("notAfter", "")
                if not_after:
                    try:
                        expiry_date = datetime.fromtimestamp(not_after / 1000)
                        ssl_result["expiry_date"] = str(expiry_date)
                        ssl_result["days_until_expiry"] = (
                            expiry_date - datetime.now()
                        ).days
                        if ssl_result["days_until_expiry"] < 30:
                            ssl_result["issues"].append("Сертификат скоро истекает")
                    except (ValueError, OSError):
                        pass

                if ssl_result["grade"] in ["F", "T"]:
                    ssl_result["issues"].append(
                        f"Низкая оценка SSL: {ssl_result['grade']}"
                    )
    except requests.RequestException as e:
        logger.error(f"Ошибка SSL Labs API: {e}")
        ssl_result["issues"].append("Сервис проверки SSL недоступен")
    result["ssl"] = ssl_result

    # ---------- 3. HTTP-заголовки ----------
    headers_result = {
        "url": url,
        "score": 0,
        "grade": "F",
        "headers_found": {},
        "issues": [],
    }
    try:
        resp = requests.get(f"https://securityheaders.com/api/v1?q={url}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            headers_result["score"] = data.get("score", 0)
            headers_result["grade"] = data.get("grade", "F")
            headers_result["headers_found"] = data.get("headers", {})
            for header in data.get("missing", {}):
                headers_result["issues"].append(f"Отсутствует заголовок: {header}")
    except requests.RequestException as e:
        logger.error(f"Ошибка SecurityHeaders API: {e}")
        headers_result["issues"].append("Сервис проверки заголовков недоступен")
    result["headers"] = headers_result

    # ---------- Итоговый вердикт ----------
    ssl_ok = ssl_result["valid_ssl"]
    headers_ok = headers_result["grade"] != "F" and headers_result["score"] > 0

    if ssl_ok and headers_ok:
        result["is_safe"] = True
        result["message"] = "Сайт безопасен: SSL и заголовки в порядке"
    else:
        reasons = []
        if not ssl_ok:
            reasons.append("проблемы с SSL")
        if not headers_ok:
            reasons.append("небезопасные HTTP-заголовки")
        result["message"] = "Сайт небезопасен: " + ", ".join(reasons)

    return result
