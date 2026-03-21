from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Row, Column, Group, Url, Start, Button
from states import StartSG, ToolSG, GuideSG, AISG
from handlers import about_bot

start_dialog = Dialog(
    Window(
        Const("Главное меню:"),
        Group(
            Button(text=Const("Что делает бот?"), id="menu_help", on_click=about_bot),
            Row(
                Start(text=Const("Инструменты"), id="menu_tool", state=ToolSG.menu),
                Start(text=Const("Справочник"), id="menu_guide", state=GuideSG.menu),
            ),
            Column(
                Start(
                    text=Const("ИИ асистент по безопасности"),
                    id="menu_ai",
                    state=AISG.first_menu,
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
