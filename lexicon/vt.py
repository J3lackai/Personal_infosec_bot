vt_fallback_e_msg = "😔 Сервис проверки ссылок временно недоступен. Попробуйте позже"
vt_error_mssgs: dict[str, str] = {
    "AuthenticationRequiredError": "🔑 Ошибка аутентификации в сервисе проверки ссылок",
    "ForbiddenError": vt_fallback_e_msg,
    "NotFoundError": "🔍 Ссылка не найдена в базе VirusTotal",
    "InvalidArgumentError": "❌ Введена некорректная ссылка. Убедитесь, что ссылка начинается с http:// или https:// ❌",
    "AlreadyExistsError": "♻️ Такая ссылка уже была отправлена на анализ ",
    "QuotaExceededError": "⏳ Превышен лимит запросов к сервису проверки. Попробуйте позже",
    "TooManyRequestsError": "⏳ Слишком много запросов к сервису. Пожалуйста, подождите немного",
    "TransientError": vt_fallback_e_msg,
    "DeadlineExceededError": "⌛ Сервис проверки не ответил вовремя. Попробуйте позже",
    "UserNotActiveError": vt_fallback_e_msg,
    "WrongCredentialsError": vt_fallback_e_msg,
}
