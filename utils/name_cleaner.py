import re

def clean_character_name(name: str) -> str:
    """
    Cleans up a character name by removing parenthetical information and stripping whitespace.
    Example: "Rem (Re:Zero)" -> "Rem"
    """
    if not isinstance(name, str):
        print(f"[DEBUG] Input to name cleaner is not a string: {name}")
        return ""

    return re.sub(r"\s*\(.*?\)", "", name).strip()