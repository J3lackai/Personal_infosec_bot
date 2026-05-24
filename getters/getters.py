from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect
from lexicon import guides

async def guide_getter(dialog_manager: DialogManager, **_):
    guides_: dict[str:str] = guides
    guides_items: list = []
    if guides is None:
        return {"guides_items": ""}
    n = 0
    n_header: dict = dict()
    for i in guides_.keys():
        guides_items.append({"id": n, "text": i})
        n_header[n] = i
        n += 1
    dialog_manager.dialog_data["n_header"] = n_header
    return {"guides_items": guides_items}

async def get_pswrd_prop(dialog_manager: DialogManager, **kwargs):
    prop = [
        ("Есть цифры", "1"),
        ("Есть спецсимволы", "2"),
        ("Есть латиница", "3"),
        ("Есть кириллица", "4"),
    ]
    return {"prop": prop}


async def get_pswrd_case(dialog_manager: DialogManager,**kwargs):
    case = [
        ("Нижний регистр", "1"),
        ("Верхний регистр", "2"),
    ]
    return {"case": case}
