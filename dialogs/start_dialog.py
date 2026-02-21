from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Column, Url, Start
from states import StartSG, ToolSG, GuideSG

start_dialog = Dialog(
    Window(
        Const("Главное меню:"),
        Column(
            Start(text=Const("🔧 Инструменты"), id="menu_tool", state=ToolSG.menu),
            Start(text=Const("📕 Справочник"), id="menu_guide", state=GuideSG.menu),
            Url(
                text=Const("✉ Связаться с разработчиком"),
                url=Const("https://t.me/artemmmat"),
                id="contact_dev",
            ),
        ),
        state=StartSG.main_menu,
    ),
)
