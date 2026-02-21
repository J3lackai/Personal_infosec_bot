from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start
from states import ToolSG, StartSG

tool_dialog = Dialog(
    Window(
        Const("Выберите инструмент:"),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="tool_start_1"),
        state=ToolSG.menu,
    ),
)
