import functools
from importlib.resources import files
from typing import Set


@functools.lru_cache(maxsize=1)
def link_shorteners_list() -> Set[str]:
    """
    Reads the built-in tracking file and returns a set of known link shortener domains.

    The results are cached in-memory after the first read to ensure O(1) performance
    with zero disk I/O overhead on later calls.

    Returns:
        Set[str]: A set containing clean, lowercase domains.
        Example: {"bit.ly", "t.co", "tinyurl.com"}
    """
    resource_path = files("antispam_link_shorteners") / "shorteners.txt"
    shorteners = set()
    with resource_path.open("r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip().lower()
            if not cleaned_line or cleaned_line.startswith("#"):
                continue
            shorteners.add(cleaned_line)
    return shorteners


__all__ = ["link_shorteners_list"]
