from aiogram_dialog import DialogManager


async def get_languages(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.find("radio_lang").get_checked()
    language = {"1": "en", "2": "ru"}
    chosen_lang = language["2" if not checked else checked]
    lang = {
        "ru": {
            "1": "🇬🇧 Английский",
            "2": "🇷🇺 Русский",
            "text": "Выберите язык",
        },
        "en": {
            "1": "🇬🇧 English",
            "2": "🇷🇺 Russian",
            "text": "Choose language",
        },
    }
    languages = [
        (f"{lang[chosen_lang]['1']}", "1"),
        (f"{lang[chosen_lang]['2']}", "2"),
    ]
    return {"languages": languages, "text": lang[chosen_lang]["text"]}
