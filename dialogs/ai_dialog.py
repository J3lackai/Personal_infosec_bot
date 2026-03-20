from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.input import TextInput, MessageInput
from states import AISG, StartSG
from aiogram.types import ContentType
from utils import promt_check
from handlers import correct_prompt, error_prompt, no_text

ai_dialog = Dialog(
    Window(
        Const("Напишите сообщение ИИ ассистенту:"),
        TextInput(
            id="ai1_input",
            type_factory=promt_check,
            on_success=correct_prompt,
            on_error=error_prompt,
        ),
        MessageInput(id="err_ai1_input", func=no_text, content_types=ContentType.ANY),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="ai_start_1"),
        state=AISG.first_menu,
    ),
    Window(
        TextInput(
            id="ai2_input",
            type_factory=promt_check,
            on_success=correct_prompt,
            on_error=error_prompt,
        ),
        MessageInput(id="err_ai2_input", func=no_text, content_types=ContentType.ANY),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="ai_start_2"),
        state=AISG.retry_menu,
    ),
)
