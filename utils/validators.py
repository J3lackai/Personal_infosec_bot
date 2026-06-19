import re

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # символы, пиктограммы, транспорт, эмодзи лиц и объектов
    "\U00002600-\U000027BF"  # разные символы (♠, ☀ и т.п.) и dingbats
    "\U0001F1E6-\U0001F1FF"  # региональные индикаторы (флаги стран)
    "\U00002700-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002300-\U000023FF"  # технические символы (⌚, ⏰ и т.п.)
    "\U0000FE0F"             # variation selector (модификатор отображения эмодзи)
    "\U0000200D"             # zero-width joiner (используется в составных эмодзи)
    "]+",
    flags=re.UNICODE,
)
def promt_validate(text: str) -> str:
    text = text.strip()

    if len(text) > 512 or len(text) == 0:
        raise ValueError

    return text

def email_validate(email:str)-> str:
    if EMOJI_PATTERN.search(email):
        raise ValueError
    if not isinstance(email, str):
        raise ValueError
    if "@" not in email or "." not in email:
        raise ValueError
    if not (6 < len(email) < 120):
        raise ValueError
    return email
def len_validate(len_str: str) -> str:
    if EMOJI_PATTERN.search(len_str):
        raise ValueError
    try:
        len = int(len_str.strip())
        if len < 12:
            raise ValueError
    except Exception:
        raise ValueError
    return len

def validate_link(link: str) -> str:
    link = link.strip()
    if EMOJI_PATTERN.search(link):
        raise ValueError
    if not re.match(r"^https?://", link):
        raise ValueError

    return link

def validate_pswrd(pswrd: str) -> str:
    if EMOJI_PATTERN.search(pswrd):
        raise ValueError
    return pswrd