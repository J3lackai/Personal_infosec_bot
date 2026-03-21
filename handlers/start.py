from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from states import StartSG
from aiogram_dialog import StartMode, DialogManager
from lexicon import about

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager):
    await message.answer("Здравствуйте!")
    await dialog_manager.start(state=StartSG.main_menu, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def command_help(message: Message):
    await message.answer(about)


async def about_bot(callback: CallbackQuery, dialog_manager: DialogManager, widget):
    await callback.answer("")
    await callback.message.answer(about)
