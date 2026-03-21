from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, Column, Select
from states import GuideSG, StartSG
from getters import guide_getter
from handlers import on_guide_select

guide_dialog = Dialog(
    Window(
        Const("❓ Выберите интересующую тему:"),
        Column(
            Select(
                Format("{item[text]}"),
                id="guides_select",
                items="guides_items",
                item_id_getter=lambda x: x["id"],
                on_click=on_guide_select,
            )
        ),
        Start(Const("🔙 Назад"), state=StartSG.main_menu, id="guides_start"),
        state=GuideSG.menu,
        getter=guide_getter,
    ),
)
