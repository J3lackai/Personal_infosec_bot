from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start, Column
from states import ToolSG, StartSG
from handlers import (
    check_links_url,
    whois_domain,
    leaks_email,
    headers_url,
    ssl_url,
    generate_password,
    check_password_strength,
)
# отключаем стандартные callback_data для примера с on_click

tool_dialog = Dialog(
    # Главное меню выбора инструмента (уже было)
    Window(
        Const("Выберите инструмент:"),
        Column(
            SwitchTo(
                text=Const(text="Проверка ссылок/сайтов"),
                state=ToolSG.check_links,
                id="SwitchTo_check_links",
            ),
            SwitchTo(text=Const(text="Whois-проверка"), state=ToolSG.whois, id="whois"),
            SwitchTo(
                text=Const(text="Проверка утечек паролей "),
                state=ToolSG.check_leaks,
                id="SwitchTo_check_leaks",
            ),
            SwitchTo(
                text=Const(text="Анализ заголовков безопасности сайта"),
                state=ToolSG.analysis_headers,
                id="SwitchTo_analysis_headlines",
            ),
            SwitchTo(
                text=Const(text="Проверка SSL сертификатов"),
                state=ToolSG.check_ssl,
                id="check_ssl",
            ),
            SwitchTo(
                text=Const(text="Генератор надёжных паролей"),
                state=ToolSG.generate_psswrd,
                id="SwitchTo_generate_psswrd",
            ),
            SwitchTo(
                text=Const(text="Проверка надежности пароля"),
                state=ToolSG.check_psswrd,
                id="SwitchTo_check_psswrd",
            ),
            Start(Const("Назад 🔙"), state=StartSG.main_menu, id="tool_start_1"),
        ),
        state=ToolSG.menu,
    ),
    # Окно: Проверка ссылок/сайтов (запрос URL)
    Window(
        Const("Введите ссылку для проверки:"),
        Button(
            text=Const(text="Отправить"),
            on_click=check_links_url,
            id="Button_check_links_url",
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_2"),
        state=ToolSG.check_links,
    ),
    # Окно: Whois-проверка (запрос домена)
    Window(
        Const("Введите имя домена для проверки:"),
        Button(
            text=Const(text="Отправить"),
            on_click=whois_domain,
            id="Button_whois_domain",
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_3"),
        state=ToolSG.whois,
    ),
    # Окно: Проверка утечек паролей (запрос email)
    Window(
        Const("Введите email для проверки на утечки:"),
        Button(
            text=Const(text="Отправить"), on_click=leaks_email, id="Button_leaks_email"
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_4"),
        state=ToolSG.check_leaks,
    ),
    # Окно: Анализ заголовков безопасности (запрос URL)
    Window(
        Const("Анализ HTTP-заголовков сайта:\nВведите адрес:"),
        Button(
            text=Const(text="Проверить"), on_click=headers_url, id="Button_headers_url"
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_5"),
        state=ToolSG.analysis_headers,
    ),
    # Окно: Проверка SSL сертификатов (запрос URL)
    Window(
        Const("Проверка SSL/TLS сертификата:\nАдрес сайта:"),
        Button(
            text=Const(text="Проверить"), on_click=ssl_url, id="Button_ssl_url"
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_6"),
        state=ToolSG.check_ssl,
    ),
    # Окно: Генератор надёжных паролей (настройка параметров)
    Window(
        Const(
            "Генерация надежного пароля:\nДлина: 12 символов\nВключить цифры? ✅\nСимволы? ✅"
        ),
        Button(
            text=Const(text="Сгенерировать"),
            on_click=generate_password,
            id="Button_generate_password",
        ),  # Хендлер принимает state и параметры длины/символами
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_7"),
        state=ToolSG.generate_psswrd,
    ),
    # Окно: Проверка надежности пароля (запрос пароля)
    Window(
        Const("Введите пароль для проверки на прочность:"),
        Button(
            text=Const(text="Проверить"),
            on_click=check_password_strength,
            id="Button_check_password_strength",
        ),  # Хендлер принимает input_text и state
        Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_8"),
        state=ToolSG.check_psswrd,
    ),
)
