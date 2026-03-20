def promt_check(text: str) -> str:
    text = text.strip()

    if len(text) > 512:
        raise ValueError

    return text
