from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from states import StartSG
from aiogram_dialog import StartMode, DialogManager

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager):
    await message.answer("Здравствуйте!")
    await dialog_manager.start(state=StartSG.main_menu, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def command_help(message: Message):
    await message.answer("Это бот")
