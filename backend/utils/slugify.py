import re

from transliterate import translit


def translit_text(text: str) -> str:
    slug = translit(text, 'ru', reversed=True)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'[^\w\-]', '', slug)
    return slug
