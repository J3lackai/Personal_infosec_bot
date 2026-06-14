from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.input import TextInput, MessageInput
from states import AISG, StartSG
from aiogram.types import ContentType
from utils import promt_validate
from getters import get_answer_groq
from handlers import correct_prompt, error_prompt, no_text

ai_dialog = Dialog(
    Window(
        Const("Напишите сообщение ИИ ассистенту:"),
        TextInput(
            id="ai1_input",
            type_factory=promt_validate,
            on_success=correct_prompt,
            on_error=error_prompt,
        ),
        MessageInput(id="err_ai1_input", func=no_text, content_types=ContentType.ANY),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="ai_start_1"),
        state=AISG.send_menu,
    ),
    Window(
        Format("{answer}"),
        TextInput(
            id="ai2_input",
            type_factory=promt_validate,
            on_success=correct_prompt,
            on_error=error_prompt,
        ),
        MessageInput(id="err_ai2_input", func=no_text, content_types=ContentType.ANY),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="ai_start_2"),
        state=AISG.answer_send_menu,
        getter=get_answer_groq,
    ),
)
