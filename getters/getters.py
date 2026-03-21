from aiogram_dialog import DialogManager


async def guide_getter(dialog_manager: DialogManager, **_):
    guides: dict[str:str] = dialog_manager.middleware_data.get("guide")
    guides_items: list = []
    if guides is None:
        return {"guides_items": ""}
    for i, j in guides.items():
        guides_items.append({"id": i, "text": j})
    return {"guides_items": guides_items}
