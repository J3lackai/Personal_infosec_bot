from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start
from states import GuideSG, StartSG

guide_dialog = Dialog(
    Window(
        Const("Выберите интересующий вопрос:"),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="guide_start_1"),
        state=GuideSG.menu,
    ),
)
