from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    main_menu = State()


class ToolSG(StatesGroup):
    menu = State()
    check_links = State()
    whois = State()
    check_leaks = State()
    analysis_headers = State()
    check_ssl = State()
    generate_psswrd = State()
    check_psswrd = State()


class GuideSG(StatesGroup):
    menu = State()


class AISG(StatesGroup):
    first_menu = State()

    retry_menu = State()
