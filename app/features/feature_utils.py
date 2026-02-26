import re


def is_bold(font_name: str) -> int:
    """
    Detect if font indicates bold style.
    """
    if not font_name:
        return 0
    return 1 if "bold" in font_name.lower() else 0


def uppercase_ratio(text: str) -> float:
    """
    Ratio of uppercase characters in text.
    """
    if not text:
        return 0.0

    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0

    uppercase_count = sum(1 for c in letters if c.isupper())
    return uppercase_count / len(letters)


def contains_numbering(text: str) -> int:
    """
    Detect heading numbering patterns like:
    1.
    1.1
    I.
    A)
    """
    pattern = r"^(\d+(\.\d+)*|[A-Z]|[IVX]+)[\.\)]"
    return 1 if re.match(pattern, text.strip()) else 0


def text_length(text: str) -> int:
    return len(text.strip())