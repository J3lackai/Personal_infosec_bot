from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    SwitchTo,
    Start,
    Column,
    Multiselect,
    Next,
    Back,
)
from states import ToolSG, StartSG
from utils import len_validate, validate_link, email_validate
import operator
from getters import get_pswrd_prop, get_pswrd_case, get_pswrd
from handlers import (
    correct_link,
    correct_site,
    correct_email,
    generate_password,
    check_password_strength,
    multiselect_clicked_prop,
    multiselect_clicked_case,
    error_len_handler,
    set_default_multiselect,
    error_link,
    error_email
)
# отключаем стандартные callback_data для примера с on_click

tool_dialog = Dialog(
        # Главное меню выбора инструмента (уже было)
        Window(
            Const("Выберите инструмент:"),
            Column(
                SwitchTo(
                    text=Const(text="Проверка ссылки"),
                    state=ToolSG.check_link,
                    id="SwitchTo_check_link",
                ),
                SwitchTo(
                    text=Const(text="Анализ безопасности сайта"),
                    state=ToolSG.analysis_site,
                    id="SwitchTo_check_site",
                ),
                SwitchTo(
                    text=Const(text="Проверка утечки почты"),
                    state=ToolSG.check_leaks,
                    id="SwitchTo_check_leaks",
                ),
                SwitchTo(
                    text=Const(text="Генератор надёжных паролей"),
                    state=ToolSG.choose_psswrd_prop,
                    id="SwitchTo_generate_psswrd",
                    on_click= set_default_multiselect
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
        # Окно: Проверка ссылки (запрос URL)
        Window(
            Const("Введите ссылку для проверки:"),
            TextInput(
                type_factory=validate_link,
                on_success=correct_link,
                on_error=error_link,
                id="input_link",
            ),
            Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_10"),
            state=ToolSG.check_link,
        ),
        # Окно: Проверка сайта (запрос URL)
        Window(
            Const("Введите ссылку на сайт для проверки:"),
            TextInput(
                type_factory=validate_link,
                on_success=correct_site,
                on_error=error_link,
                id="input_link",
            ),
            Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_2"),
            state=ToolSG.analysis_site,
        ),
        # Окно: Проверка утечек паролей (запрос email)
        Window(
            Const("Введите email для проверки на утечки:"),
            TextInput(on_success=correct_email, on_error=error_email, type_factory=email_validate, id="textinput_leak"),
            Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_4"),
            state=ToolSG.check_leaks,
        ),
        # Окно: Генератор надёжных паролей (настройка параметров)
        Window(
            Const(
                "Какие символы будут в вашем пароле:\n(Выберите как минимум 3 галочки)"
            ),
            Column(
                Multiselect(
                    checked_text=Format("[✔️] {item[0]}"),
                    unchecked_text=Format("[❌] {item[0]}"),
                    id="pswrd_prop",
                    item_id_getter=operator.itemgetter(1),
                    items="prop",
                    min_selected=3,
                    on_state_changed=multiselect_clicked_prop,
                ),
                Next(text=Const(text="Далее")),
                Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_7"),
            ),
            getter=get_pswrd_prop,
            state=ToolSG.choose_psswrd_prop,
        ),
        Window(
            Const("Выбор регистра:\n(Выберите хотя бы один)"),
            Column(
                Multiselect(
                    checked_text=Format("[✔️] {item[0]}"),
                    unchecked_text=Format("[❌] {item[0]}"),
                    id="high_lower_case",
                    item_id_getter=operator.itemgetter(1),
                    items="case",
                    min_selected=1,
                    on_state_changed=multiselect_clicked_case,
                ),
                Next(
                    text=Const(text="Далее"),
                ),
                Back(
                    Const("Назад 🔙"),
                ),
            ),
            getter=get_pswrd_case,
            state=ToolSG.choose_psswrd_case,
        ),
        Window(
            Const(
                "Напишите какой длины пароль вы хотите:\n(Напишите только число. Минимальная длина: 12)"
            ),
            TextInput(
                id="len_input",
                type_factory=len_validate,
                on_success=generate_password,
                on_error=error_len_handler,
            ),
            Back(
                Const("Назад 🔙"),
            ),
            state=ToolSG.choose_len_psswrd,
        ),
        Window(
            Format("Ваш безопасный пароль: {pswrd}"),
            SwitchTo(Const("Сгенерировать ещё один пароль 🔁"), state=ToolSG.choose_psswrd_prop, id="switchto_retry"),
            Start(Const("В меню 🏠"), state=StartSG.main_menu, id="tool_start_9"),
            state=ToolSG.result, getter=get_pswrd),
        # Окно: Проверка надежности пароля (запрос пароля)
        Window(
            Const("Введите пароль для проверки на прочность:"),
            TextInput(
                on_success=check_password_strength,
                id="input_psswrd",
            ),  # Хендлер принимает input_text и state
            Start(Const("Назад 🔙"), state=ToolSG.menu, id="tool_start_8"),
            state=ToolSG.check_psswrd,
        ),
)
