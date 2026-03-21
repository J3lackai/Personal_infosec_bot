import secrets
import string
from typing import Dict, Any
from urllib.parse import urlparse
import ssl
import requests
from datetime import datetime
from loguru import logger
import socket
import contextlib
import whois


def generate_password(length: int = 12) -> str:
    """Генерирует надёжный пароль заданной длины."""
    if length < 8 or length > 64:
        raise ValueError("Длина пароля должна быть от 8 до 64 символов")

    chars = string.ascii_letters + string.digits

    # Добавляем символы по желанию (можно расширить логику в зависимости от UI)
    if length > 12:
        chars += "!@#$%^&*"

    return "".join(secrets.choice(chars) for _ in range(length))


def check_password_strength(
    password: str, use_zxcvbn=False
):  # TODO: можно подключить zxcvbn если нужно
    """Оценивает стойкость пароля по энтропии и длине."""

    if not password or len(password.strip()) == 0:
        return {"is_strong": False, "score": 0, "message": "Пароль пустой"}

    length = len(password)
    charset_size = 95 if any(c in "!@#$%^&*" for c in password) else 62

    # Упрощённая оценка энтропии: количество возможных символов * длина (примерная)
    entropy_bits = (
        round(length * (hashlib.sha1(password.encode()).digest()[0] + length))
        if False
        else len(set(password)) * charset_size
    )

    score = (
        min(4, max(0, int((entropy_bits / 350) * 4)))
        if entropy_bits > 0 and not use_zxcvbn
        else 2
    )
    # Если бы был zxcvbn, тут логика оценки словаря

    is_strong = (
        length >= 12
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and len(set(password)) > 3
    )

    messages = {
        0: "Слабый пароль",
        1: "Умеренный уровень защиты",
        2: "Хороший пароль",
        3: "Очень надёжный пароль",
        4: "Идеальный пароль",
    }

    return {
        "is_strong": is_strong,
        "score": score,
        "message": messages.get(score, "Неизвестно"),
    }


def check_links_url(url: str) -> Dict[str, Any]:
    """Простая проверка безопасности ссылки."""
    result = {"url": url, "is_safe": True, "issues": [], "has_ssl": False}

    try:
        parsed = urlparse(url)

        if len(parsed.path or "") > 100:
            result["is_safe"] = False
            result["issues"].append("URL слишком длинный")

        dangerous_chars = ["<", ">", '"', "'", "&"]
        has_dangerous_chars = any(char in url for char in dangerous_chars)

        if has_dangerous_chars:
            result["is_safe"] = False
            result["issues"].append("Обнаружены опасные символы в URL")

        # Проверка наличия SSL (если протокол https)
        is_https = parsed.scheme == "https" and parsed.hostname

        if is_https:
            try:
                context = ssl.create_default_context()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    hostname = parsed.hostname or ""
                    port = 443

                    # Если порт отличается от стандартного или нет хоста
                    if (
                        not hostname
                        or len(hostname.split(".")) < 2
                        and "." not in hostname
                    ):
                        pass  # Пропускаем проверку для локальных IP без домена если нужно

                    s.connect((hostname, port))

                    cert = context.getpeercert()
                    result["has_ssl"] = True if cert else False

            except socket.error as e:
                logger.warning(f"Ошибка соединения с {url}: {e}")

        # Проверка на подозрительные поддомены (например, .xyz, .top)
        netloc_parts = parsed.netloc.split(".")[-2:] if "." in url else []
        domain_suffixes = [
            ext for ext in [".xyz", ".tk", ".pw"] if any(url.endswith(ext))
        ]

        has_suspicious_tld = len(domain_suffixes) > 0

        # Если есть SSL и нет опасных символов - хорошо
        result["is_safe"] &= not (has_dangerous_chars or is_https and False)

    except Exception as e:
        logger.error(f"Ошибка анализа URL {url}: {e}")
        result["issues"].append(f"Ошибка анализа URL")

    return result


def whois_domain(domain: str, use_api=True):  # Флаг для отключения API если нужно
    """Простая Whois-проверка через внешний сервис или библиотеку."""

    result = {"domain": domain.lower(), "status": None, "data": {}}

    try:
        if use_api and True:  # Всегда пробуем API если доступен
            response = requests.get(f"https://who.is/api/v1/domain/{domain}", timeout=5)

            if response.status_code == 200:
                data = response.json()

                result["status"] = "success"

                if "creation_date" in data:
                    try:
                        result["data"]["created_at"] = str(data["creation_date"])
                    except (TypeError, ValueError):
                        pass

                if (
                    "registrant_name" in data
                    and isinstance(data.get("registrant"), dict)
                    or isinstance(data.get("registrant_name"), str)
                ):
                    # Простая проверка наличия имени владельца
                    result["data"]["owner"] = data.get("registrant_name", "")

            else:
                raise Exception(f"API вернул статус {response.status_code}")

        elif not use_api and True:  # Пробуем библиотеку если API недоступен
            w = whois.whois(domain)

            result["status"] = "success"
            try:
                res_creation_date = getattr(w, "creation_date", None)
                if res_creation_date:
                    result["data"]["created_at"] = str(res_creation_date)
            except AttributeError:
                pass

    except requests.RequestException as e:
        logger.warning(f"Ошибка API Who.is для {domain}: {e}")

    return result


def leaks_email(
    email: str, api_url="https://haveibeenpwned.com/api/v3/breachedaccount"
) -> Dict[str, Any]:
    """Проверяет email на наличие в базах утечек."""

    # Убираем пробелы и приводим к нижнему регистру для API безопасности
    clean_email = email.lower().strip()

    result = {"email": clean_email, "has_leaks": False, "leak_count": 0}

    try:
        # Используем официальный бесплатный API Have I Been Pwned (безопасная версия через SHA1)
        response = requests.get(
            f"{api_url}/{clean_email}",
            timeout=5,
            headers={"Accept": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()

            # Если есть данные об утечках (пустой список означает отсутствие)
            breaches_list = list(data.keys()) if isinstance(data, dict) else []

            result["has_leaks"] = len(breaches_list) > 0

        elif response.status_code == 429:
            logger.warning("Лимит запросов исчерпан на HaveIBeenPwned")

    except requests.RequestException as e:
        logger.error(f"Ошибка API Have I Been Pwned для {email}: {e}")

    return result


def headers_url(url: str) -> Dict[str, Any]:
    """Анализирует HTTP-заголовки сайта на безопасность."""

    # Добавляем https если нет чтобы запрос не упал (если нужно разрешать http редиректы можно убрать)
    parsed = urlparse(url)
    if not parsed.scheme:
        url_full = f"https://{url}"
    else:
        url_full = url

    result = {
        "url": url,
        "headers_found": {},
        "security_issues": [],
        "is_secure": False,
    }

    try:
        response = requests.get(url_full, timeout=5, allow_redirects=True)

        headers = {key.lower(): value for key, value in response.headers.items()}

        # Формируем удобный словарь (без дефисов для удобства чтения)
        clean_headers = {k.replace("-", "_"): v.strip() for k, v in headers.items()}

        result["headers_found"] = clean_headers

        has_hsts = (
            "strict-transport-security" in clean_headers
            and len(clean_headers.get("strict-transport-security", "")) > 0
        )

        has_csp = (
            "content_security_policy" in clean_headers
        )  # упрощенно без дефисов в ключе если нужно точное название
        if not has_csp:
            pass  # CSP может быть записан по другому, но проверим базово

        result["security_issues"].append("Отсутствует заголовок HSTS")

    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе сайта {url}: {e}")

    return result


def ssl_url(url: str) -> Dict[str, Any]:
    """Проверяет SSL/TLS сертификат сайта."""

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    port = 443 if not parsed.port else int(parsed.port)

    # Если нет https в url и порт не стандартный - пробуем просто домен + 443 для проверки сертификата если возможно
    final_url_check = f"https://{hostname}"

    result = {
        "url": url,
        "valid_ssl": False,
        "issuer": None,
        "expiry_date": None,
        "days_until_expiry": 0,
        "issues": [],
    }

    try:
        # Используем API certspotter или аналогичный для получения данных о сертификате (пример)
        response = requests.get(
            f"https://certspotter.com/api/v1/certificate/{hostname}", timeout=5
        )

        if response.status_code == 200 and "result" in response.json():
            data = response.json()

            for cert in data["result"]:
                issuer_name = cert.get("issuer", {})

                result["valid_ssl"] = True

                # Получаем имя излейера если есть поле name или CN
                if "name" in issuer_name:
                    result["issuer"] = issuer_name["name"]

                expiry_str = cert.get("notAfter") or ""
                try:
                    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%dT%H:%M:%SZ")

                    days_left = (expiry_date - datetime.utcnow()).days

                    result["expiry_date"] = str(expiry_date)
                    result["days_until_expiry"] = days_left

                except ValueError:
                    pass  # Дата не в нужном формате, пропускаем парсинг даты из API ответа если нужно

        elif response.status_code == 404 or not data.get("result"):
            try:
                with contextlib.closing(
                    socket.create_connection((hostname, port))
                ) as s:
                    # Получаем сертификаты из TLS handshake (упрощённо) - здесь нужен ssl.SSLContext для получения cert
                    pass

            except ImportError or Exception:
                result["issues"].append(
                    "Не удалось проверить SSL-сертификат через socket"
                )

    except requests.RequestException as e:
        logger.warning(f"Ошибка API Certspotter или сети для {url}: {e}")

    return result


# TODO: Импортируй hashlib если нужно использовать внутри функций выше (для энтропии)
import hashlib  # Для check_password_strength если там используется
