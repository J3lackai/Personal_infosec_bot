from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    main_menu = State()
    about_bot = State()


class ToolSG(StatesGroup):
    menu = State()
    check_link = State()
    analysis_site = State()
    check_leaks = State()
    choose_psswrd_prop = State()
    choose_psswrd_case = State()
    choose_len_psswrd = State()
    generate_psswrd = State()
    input_psswrd = State()
    check_psswrd = State()


class GuideSG(StatesGroup):
    menu = State()
    answer = State()


class AISG(StatesGroup):
    first_menu = State()

    retry_menu = State()
