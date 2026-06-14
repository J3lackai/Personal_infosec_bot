from aiogram_dialog import DialogManager
from config import Services
from aiogram.types import Message
async def send_msg_dev(message: Message, widget, dialog_manager: DialogManager, value: str):
    services: Services = dialog_manager.middleware_data.get(
            "external_services"
        )
    await dialog_manager.next()
    user_info = "Вам написал пользователь бота Personal_isec_bot: \n"
    await message.bot.send_message(chat_id=services.telegram_id_dev, 
                                   text = user_info + value)
    
    