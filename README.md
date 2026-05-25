# 🛡️ Personal InfoSec Bot

Telegram-бот персональной информационной безопасности для обычного пользователя.  
Объединяет **ИИ-ассистента**, набор **практических инструментов** и **справочник по ИБ** в одном месте — прямо в мессенджере, без лишних порогов входа.

---

## ✨ Возможности

### 🤖 ИИ-ассистент
Чат с LLM (Qwen3-32b через Groq API) — задавай вопросы по информационной безопасности, получай советы и объяснения в свободной форме.

### 🔍 Инструменты

| Инструмент | Описание |
|---|---|
| 🔗 Проверка URL | Анализ ссылки на фишинг и вредоносное ПО |
| 💧 Breach Scan | Проверка email по базам утечек через HaveIBeenPwned |
| 🔒 SSL/TLS проверка | Валидность сертификата, дата истечения, issuer |
| 🔑 Генератор паролей | Сложные пароли заданной длины и набора символов |
| 💪 Анализатор паролей | Оценка стойкости пароля (энтропия) |
| 🛡️ Заголовки безопасности | Проверка наличия SSL, HSTS, CSP и других заголовков |

### 📚 Справочник по ИБ
Структурированная база знаний по основным угрозам, терминам и методам защиты.

---

## 🛠️ Стек

- **Python 3.11+**
- **aiogram 3** — фреймворк для Telegram Bot API
- **aiogram-dialog** - надстройка над фреймворком aiogram

---

## 🚀 Запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/J3lackai/Personal_infosec_bot.git
cd Personal_infosec_bot
```

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```

### 3. Настрой переменные окружения

Создай файл `.env` на основе `.env.example`:

```env
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
HIBP_API_KEY=your_haveibeenpwned_api_key
```

- **BOT_TOKEN** — получи у [@BotFather](https://t.me/BotFather)
- **GROQ_API_KEY** — зарегистрируйся на [console.groq.com](https://console.groq.com)

### 4. Запусти бота

```bash
python main.py
```

---

## 📁 Структура проекта

```
Personal_infosec_bot/
├── config/          # Конфигурация и настройки
├── dialogs/         # Диалоги и сценарии
├── filters/         # Фильтры сообщений
├── getters/         # Геттеры данных
├── handlers/        # Обработчики команд и сообщений
├── keyboards/       # Клавиатуры и инлайн-кнопки
├── lexicon/         # Тексты и сообщения бота
├── middlewares/     # Промежуточные обработчики
├── states/          # FSM-состояния
├── utils/           # Вспомогательные утилиты
├── main.py          # Точка входа
└── requirements.txt
```

---

## 🔑 Необходимые API-ключи

| Сервис | Для чего | Ссылка |
|---|---|---|
| Telegram Bot API | Работа бота | [@BotFather](https://t.me/BotFather) |
| Groq API | ИИ-ассистент (бесплатно) | [console.groq.com](https://console.groq.com) |
| HaveIBeenPwned | Проверка утечек | [haveibeenpwned.com](https://haveibeenpwned.com/API/Key) |

---

## 👤 Автор

**J3lackai** — [GitHub](https://github.com/J3lackai)
