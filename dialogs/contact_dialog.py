from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.input import TextInput
from states import ContactDev, StartSG
from handlers import send_msg_dev
contact_dialog = Dialog(
    Window(
        Const("Напишите сообщение, " \
        "оно будет передано разработчику"),
        TextInput(on_success=send_msg_dev, id="contact_text_input"),
        Start(Const("Назад 🔙"), state=StartSG.main_menu, id="cntct_start_1"),
    state=ContactDev.send_message),
    Window(Const("Ваше сообщение скоро будет доставлено разработчику!"),
           Start(Const("Назад 🔙"), state=StartSG.main_menu, id="cntct_start_2"), 
           state=ContactDev.complete,
           ),
    
    )
    

