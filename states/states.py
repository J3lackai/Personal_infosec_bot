from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    main_menu = State()


class ToolSG(StatesGroup):
    menu = State()


class GuideSG(StatesGroup):
    menu = State()


class LanguageSG(StatesGroup):
    menu = State()


class AISG(StatesGroup):
    first_menu = State()

    retry_menu = State()
