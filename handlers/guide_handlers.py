from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from lexicon import guide


async def on_guide_select(
    callback: CallbackQuery, widget, manager: DialogManager, item_id: str
):
    callback.answer(" dfdfdf")
    callback.message.answer(guide["item_id"])
