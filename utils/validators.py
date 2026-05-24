import re
def promt_validate(text: str) -> str:
    text = text.strip()

    if len(text) > 512 or len(text) == 0:
        raise ValueError

    return text


def len_validate(len_str: str) -> str:
    try:
        len = int(len_str.strip())
        if len < 12:
            raise ValueError
    except Exception:
        raise ValueError
    return len

def validate_link(link: str) -> str:
    link = link.strip()

    if not re.match(r"^https?://", link):
        raise ValueError

    return link