import unidecode


def clean_string(text: str, clean_white_space=True) -> str:
    text = unidecode.unidecode(text)
    text = text.casefold().strip()
    if clean_white_space:
        text = text.replace(' ', '')
    return text


def slugify(text: str) -> str:
    text = unidecode.unidecode(text)
    text = text.casefold().strip().replace(' ', '-')
    return text
