import re

def clean_character_names(character_names):
    """
    Cleans a list of character names by removing any text within parentheses and stripping whitespace.
    
    Args:
        character_names (list): List of character names as strings.
        
    Returns:
        list: Cleaned list of character names.
    """
    return [
        re.sub(r"\s*\(.*?\)", "", name).strip()
        for name in character_names
    ]