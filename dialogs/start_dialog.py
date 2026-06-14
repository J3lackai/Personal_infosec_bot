from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Row, Column, Group, Url, Start, Next, Back
from states import StartSG, ToolSG, GuideSG, AISG, ContactDev
from lexicon import about

start_dialog = Dialog(
    Window(
        Const("Главное меню:"),
        Group(
            Next(text=Const("Что делает бот?"), id="menu_help"),
            Row(
                Start(text=Const("Инструменты"), id="menu_tool", state=ToolSG.menu),
                Start(text=Const("Справочник"), id="menu_guide", state=GuideSG.menu),
            ),
            Column(
                Start(
                    text=Const("ИИ асистент по безопасности"),
                    id="menu_ai",
                    state=AISG.send_menu,
                ),
                Start(
                    text=Const("Связаться с разработчиком"),
                    state=ContactDev.send_message,
                    id="contact_dev",
                ),
            ),
        ),
        state=StartSG.main_menu,
    ),
    Window(
        Const(text=about),
        Back(Const("🔙 Назад"), id="menu_back"),
        state=StartSG.about_bot,
    ),
)
