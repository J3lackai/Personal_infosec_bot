from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start
from states import AISG, StartSG

ai_dialog = Dialog(
    Window(
        Const("Напишите интересующий вас вопрос:"),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="ai_start_1"),
        state=AISG.menu,
    ),
)
