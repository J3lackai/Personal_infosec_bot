import vt
import socket
from urllib.parse import urlparse
import requests
from aiogram.types import Message
from datetime import datetime
from loguru import logger
import asyncio
from lexicon import vt_error_mssgs, vt_fallback_e_msg

async def correct_site(
    message: Message,
    widget,
    dialog_manager,
    url: str,
) -> None:
    import ssl

    SECURITY_HEADERS = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    parsed = urlparse(url)
    hostname = parsed.hostname or url

    # ---------- SSL (прямая проверка) ----------
    ssl_result = {
        "valid_ssl": False,
        "issuer": "",
        "expiry_date": "",
        "days_until_expiry": 0,
        "issues": [],
    }
    try:
        def _check_ssl():
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.settimeout(10)
                s.connect((hostname, 443))
                return s.getpeercert()

        cert = await asyncio.to_thread(_check_ssl)

        expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.now()).days
        ssl_result["expiry_date"] = str(expiry)
        ssl_result["days_until_expiry"] = days_left
        ssl_result["issuer"] = dict(x[0] for x in cert["issuer"]).get("organizationName", "")
        ssl_result["valid_ssl"] = True

        if days_left < 30:
            ssl_result["issues"].append("Сертификат скоро истекает")

    except ssl.SSLCertVerificationError:
        ssl_result["issues"].append("Сертификат недействителен")
    except ssl.SSLError as e:
        ssl_result["issues"].append(f"Ошибка SSL: {e}")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        if "getaddrinfo failed" in str(e):
            ssl_result["issues"].append("Сайт недоступен или не существует")
        else:
            ssl_result["issues"].append("Не удалось подключиться")
        logger.error(f"Ошибка SSL-проверки {hostname}: {e}")
    # ---------- HTTP-заголовки (прямая проверка) ----------
    headers_result = {
        "score": 0,
        "found": [],
        "issues": [],
    }
    try:
        resp = await asyncio.to_thread(
            requests.get, url, timeout=10, allow_redirects=True
        )
        found, missing = [], []
        resp_headers_lower = {k.lower() for k in resp.headers}

        for header in SECURITY_HEADERS:
            if header.lower() in resp_headers_lower:
                found.append(header)
            else:
                missing.append(header)
                headers_result["issues"].append(f"Отсутствует: {header}")

        headers_result["found"] = found
        score = len(found) / len(SECURITY_HEADERS)
        headers_result["score"] = round(score * 10)

    except requests.RequestException as e:
        if "NameResolutionError" in str(e) or "getaddrinfo failed" in str(e):
            logger.error(f"DNS не резолвится для {url}: {e}")
            headers_result["issues"].append("Сайт недоступен или не существует")
        else:
            logger.error(f"Ошибка проверки заголовков {url}: {e}")
            headers_result["issues"].append("Не удалось подключиться к сайту")
    # ---------- Итоговый вердикт ----------
    ssl_ok = ssl_result["valid_ssl"]
    headers_ok = headers_result["score"] > 5

    if ssl_ok and headers_ok:
        verdict_text = "✅ Сайт безопасен: SSL и заголовки в порядке"
    else:
        reasons = []
        if not ssl_ok:
            reasons.append("проблемы с SSL")
        if not headers_ok:
            reasons.append("небезопасные HTTP-заголовки")
        verdict_text = "⚠ Сайт содержит недостатки конфигурации: " + ", ".join(reasons)

    # ---------- Ответ пользователю ----------
    ssl_lines = [
        f"🔒 SSL: {'✅ действителен' if ssl_ok else '❌ недействителен'}",
        f"  Издатель: {ssl_result['issuer'] or '—'}",
        f"  Истекает: {ssl_result['expiry_date'] or '—'} ({ssl_result['days_until_expiry']} дн.)",
    ]
    if ssl_result["issues"]:
        ssl_lines += [f"  ⚠️ {i}" for i in ssl_result["issues"]]

    headers_lines = [
        f"🛡 HTTP-заголовки: оценка: {headers_result['score']}/10",
        f"  Найдено {len(headers_result['found'])}/{len(SECURITY_HEADERS)}",
    ]
    if headers_result["issues"]:
        headers_lines += [f"  ⚠️ {i}" for i in headers_result["issues"]]

    text = "\n".join([
        f"🌐 Проверка сайта: {url}",
        "",
        *ssl_lines,
        "",
        *headers_lines,
        "",
        verdict_text,
    ])

    await message.answer(text)

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

async def error_link(message: Message, widget, manager, error):
    await message.answer("❌ Введите корректную ссылку\nПример: https://example.com")
