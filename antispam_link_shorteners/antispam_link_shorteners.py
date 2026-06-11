"""Check and validate URLs against a link shortener blacklist."""

import functools
from importlib.resources import files
from urllib.parse import urlparse


@functools.lru_cache(maxsize=1)
def link_shorteners_list() -> set[str]:
    """Read the built-in tracking file and return known shortener domains.

    The results are cached in-memory after the first read to ensure O(1)
    performance with zero disk I/O overhead on later calls.

    Returns:
        set[str]: A set containing clean, lowercase domains.
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


def is_link_shortener(url: str) -> bool:
    """Check if the provided URL or domain belongs to a known link shortener.

    This method normalizes the input by stripping whitespace, converting it
    to lowercase, removing 'www.' prefixes, and extracting the core domain
    (a.tld) regardless of whether the protocol (http/https) or trailing
    paths are present.

    Args:
        url (str): The URL or domain string to validate and check.
            Examples: 'https://www.bit.ly/abc', 'bit.ly', 'www.t.co'

    Returns:
        bool: True if the extracted domain is in the link shorteners
            blacklist, False otherwise.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input is empty, blank, or does not represent a
            valid URL/domain structure (e.g., missing a TLD dot).

    """
    if not isinstance(url, str):
        msg = f"Expected a string, got {type(url).__name__}"
        raise TypeError(msg)

    url_clean = url.strip()
    if not url_clean:
        msg = "URL string cannot be empty or blank."
        raise ValueError(msg)

    url_lower = url_clean.lower()

    if not url_lower.startswith(("http://", "https://")):
        parsed_url = urlparse(f"https://{url_lower}")
    else:
        parsed_url = urlparse(url_lower)

    hostname = parsed_url.hostname

    if not hostname:
        msg = f"The provided value '{url}' is not a valid URL or domain."
        raise ValueError(msg)

    hostname = hostname.removeprefix("www.")

    if "." not in hostname:
        msg = f"The provided value '{url}' is not a valid URL or domain."
        raise ValueError(msg)

    return hostname in link_shorteners_list()


__all__ = ["is_link_shortener", "link_shorteners_list"]
