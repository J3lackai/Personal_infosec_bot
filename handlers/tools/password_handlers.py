import secrets
import string
import re
from aiogram_dialog.widgets.kbd import ManagedMultiselect
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from loguru import logger

async def check_password_strength(
    message: Message,
    widget,
    manager: DialogManager,
    value: int,
):
    """Анализирует пароль и отправляет результат пользователю."""

    tips = []
    score = 0
    psswrd = (message.text).strip()
    logger.info(psswrd)

    # Длина
    length = len(psswrd)
    if length < 12:
        score += 1
        tips.append("⚠️ Рекомендуется от 12 символов")
    elif length < 16:
        score += 2
    else:
        score += 3

    # Регистр
    has_upper_eng = bool(re.search(r"[A-Z]", psswrd))
    has_lower_eng = bool(re.search(r"[a-z]", psswrd))
    has_upper_ru = bool(re.search(r"[А-ЯЁ]", psswrd))
    has_lower_ru = bool(re.search(r"[а-яё]", psswrd))
    no_words = not (has_upper_eng or has_lower_eng or has_upper_ru or has_lower_ru)
    no_upper_lower = not (has_upper_eng and (has_lower_ru or has_lower_eng)or has_upper_ru and (has_lower_ru or has_lower_eng))
    no_eng = not (has_upper_eng or has_lower_eng)
    no_ru = not (has_upper_ru or has_lower_ru)
    if no_words:
        tips.append("❌ Нет букв")
    elif no_upper_lower:
        tips.append("⚠️ Используйте буквы обоих регистров")
        score+=1
    elif no_eng:
        tips.append("❌ Нет английских букв")
        score+=2
    elif no_ru:
        tips.append("❌ Нет русских букв")
        score+=2
    else:
        score+=4
    # Цифры
    if re.search(r"\d", psswrd):
        score += 1
    else:
        tips.append("❌ Нет цифр")

    # Спецсимволы
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", psswrd):
        score += 2
    else:
        tips.append("❌ Нет спецсимволов (!@#$%^&* и др.)")

    # Повторы
    if re.search(r"(.)\1{2,}", psswrd):
        score -= 1
        tips.append("⚠️ Есть повторяющиеся символы (aaa, 111...)")

    # Частые паттерны
    common_sequences = ["123456", "qwerty", "abcdef", "111111", "password", "qweasd"]
    if any(seq in psswrd.lower() for seq in common_sequences):
        score -= 2
        tips.append("❌ Содержит очевидную последовательность")

    # Только цифры
    if re.fullmatch(r"\d+", psswrd):
        score -= 1
        tips.append("❌ Пароль состоит только из цифр")

    score = max(0, score)

    # Уровень
    if score <= 2:
        level = "🔴 Очень слабый"
    elif score <= 4:
        level = "🟠 Слабый"
    elif score <= 6:
        level = "🟡 Средний"
    elif score <= 8:
        level = "🟢 Сильный"
    else:
        level = "💪 Очень сильный"

    # 👇 ОТПРАВКА РЕЗУЛЬТАТА
    text = (
        f"🔐 Пароль: `{psswrd}`\n"
        f"📊 Уровень: {level}\n"
        f"⭐ Оценка: {score}/10\n\n"
    )

    if tips:
        text += "💡 Рекомендации:\n" + "\n".join(tips)
    await message.answer(text)

async def generate_password(
    message: Message,
    widget,
    dialog_manager: DialogManager,
    value
) -> str:
    """Генерирует надёжный пароль по выбранным параметрам"""

    list_prop = dialog_manager.dialog_data.get("list_checked_prop", [])
    list_case = dialog_manager.dialog_data.get("list_checked_case", [])
    len_pswrd = int(dialog_manager.dialog_data.get("len_psswrd", 12))

    chars = ""
    specsym="!@#$%^&*()_+-=[]{}|;:,.<>?"
    lower_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    upper_ru = lower_ru.upper()

    # Используем паттерн dispatch table, формируем словарь

    dict_prop = {"3":{"1":string.ascii_lowercase, "2":string.ascii_uppercase}, # Латиница
                 "1":string.digits, # Цифры
                 "2":specsym, # Спецсимволы
                 "4":{"1":lower_ru, "2":upper_ru}} # Кириллица
    for s in list_prop:
        value : dict | str= dict_prop[s]
        if isinstance(value,dict):
            for i in list_case:
                chars+=value[i]
        else:
            chars+=value

    # Если пользователь ничего не выбрал
    if not chars:
        chars = string.ascii_letters + string.digits

    pswrd = "".join(secrets.choice(chars) for _ in range(len_pswrd))
    await dialog_manager.next()
    dialog_manager.dialog_data["pswrd"] = pswrd

async def set_default_multiselect(    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager):

    multiselect = dialog_manager.find("high_lower_case")
    await multiselect.set_checked("1", True)
    await multiselect.set_checked("2", True)

    multiselect = dialog_manager.find("pswrd_prop")
    await multiselect.set_checked("1", True)
    await multiselect.set_checked("2", True)
    await multiselect.set_checked("3", True)
    await multiselect.set_checked("4", True)

async def multiselect_clicked_prop(
    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager,
    value: str,

):
    dialog_manager.dialog_data.update(list_checked_prop=multiselect.get_checked())


async def multiselect_clicked_case(
    callback: CallbackQuery,
    multiselect:ManagedMultiselect,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data.update(list_checked_case=multiselect.get_checked())


async def error_len_handler(message: Message, widget, manager, error):
    await message.answer("❌ Введите только число\nПример: 12")

async def incorrect_pswrd(message: Message, widget, manager, error):
    await message.answer("❌ Пароль не должен содержать эмоджи!")