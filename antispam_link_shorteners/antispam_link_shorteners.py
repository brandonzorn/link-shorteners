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
    """Check if the provided URL belongs to a known link shortener.

    This method normalizes the input by stripping whitespace, converting it
    to lowercase, removing 'www.' prefixes, and extracting the core domain
    (a.tld).

    Args:
        url (str): The URL or domain string to validate and check.
            Examples: 'https://www.bit.ly/abc', 'ftp://bit.ly', 'smth://www.t.co'

    Returns:
        bool: True if the extracted domain is in the link shorteners
            blacklist, False otherwise.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input is empty, blank, or does not represent a
            valid URL/domain structure (e.g., missing protocol or a TLD dot).

    """
    if not isinstance(url, str):
        msg = f"Expected a string, got {type(url).__name__}"
        raise TypeError(msg)

    url_clean = url.strip().lower()
    if not url_clean:
        msg = "URL string cannot be empty or blank."
        raise ValueError(msg)

    if "://" not in url_clean:
        url_clean = "http://" + url_clean

    parsed_url = urlparse(url_clean)
    hostname = parsed_url.hostname

    if hostname and hostname.startswith("www."):
        hostname = hostname.removeprefix("www.")

    if not parsed_url.scheme or not hostname or "." not in hostname:
        msg = f"The provided value '{url}' is not a valid URL."
        raise ValueError(msg)

    return (
        hostname in link_shorteners_list()
        or f"www.{hostname}" in link_shorteners_list()
    )


__all__ = ["is_link_shortener", "link_shorteners_list"]
