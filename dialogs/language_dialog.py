from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Column, Radio, Start
import operator
from states import LanguageSG, StartSG
from getters import get_languages

language_dialog = Dialog(
    Window(
        Format(text="{text}"),
        Column(
            Radio(
                checked_text=Format("🔘 {item[0]}"),
                unchecked_text=Format("⚪️ {item[0]}"),
                id="radio_lang",
                item_id_getter=operator.itemgetter(1),
                items="languages",
            ),
        ),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="language_start"),
        state=LanguageSG.menu,
        getter=get_languages,
    ),
)
