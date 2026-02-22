from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Row, Column, Group, Url, Start
from states import StartSG, ToolSG, GuideSG, LanguageSG

start_dialog = Dialog(
    Window(
        Const("Главное меню:"),
        Group(
            Row(
                Start(text=Const("Инструменты"), id="menu_tool", state=ToolSG.menu),
                Start(text=Const("Справочник"), id="menu_guide", state=GuideSG.menu),
            ),
            Column(
                Start(
                    text=Const("Выбор языка / Сhoose language"),
                    id="menu_language",
                    state=LanguageSG.menu,
                ),
                Url(
                    text=Const("Контакт разработчика"),
                    url=Const("https://t.me/artemmmat"),
                    id="contact_dev",
                ),
            ),
        ),
        state=StartSG.main_menu,
    ),
)
