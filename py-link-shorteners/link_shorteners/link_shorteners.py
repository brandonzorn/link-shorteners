from importlib.resources import read_text
from typing import List

def link_shorteners_list() -> List[str]:
    """
    Returns:
        List[str]: A list containing link shorteners collected so far.
        eg. ['bit.ly/', 'ow.ly/']
    """
    data = read_text('link_shorteners', 'link-shorteners.txt', encoding='utf-8')
    return list({line.strip() for line in data.splitlines() if line.strip()})
