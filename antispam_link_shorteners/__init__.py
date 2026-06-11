"""Antispam Link Shorteners package for detecting blacklisted domains."""

from .antispam_link_shorteners import is_link_shortener, link_shorteners_list

__all__ = ["is_link_shortener", "link_shorteners_list"]
