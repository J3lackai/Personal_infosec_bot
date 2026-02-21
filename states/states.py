from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    main_menu = State()


class ToolSG(StatesGroup):
    menu = State()


class GuideSG(StatesGroup):
    menu = State()
