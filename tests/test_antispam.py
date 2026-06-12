"""Unit tests for the antispam link shortener detection module."""

import unittest
from unittest.mock import patch

from antispam_link_shorteners import is_link_shortener


class TestIsBlocked(unittest.TestCase):
    """Test suite for the is_blocked utility function."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up mocked shorteners data before running any tests."""
        cls.mocked_shorteners = {
            "bit.ly",
            "t.co",
            "tinyurl.com",
            "is.gd",
        }
        cls.patcher = patch(
            "antispam_link_shorteners.link_shorteners_list",
            return_value=cls.mocked_shorteners,
        )
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the patcher active during the test lifecycle."""
        cls.patcher.stop()

    def test_blocked_links_various_formats(self) -> None:
        """Verify known link shorteners trigger a blocked status."""
        test_cases = [
            "http://bit.ly",
            "http://BIT.LY",
            "  http://bit.ly  ",
            "http://www.bit.ly",
            "http://bit.ly",
            "https://www.bit.ly",
            "https://bit.ly/some/path?param=1",
            "http://WWW.BIT.LY/abc",
            "http://u.to",
            "http://u.shxj.pw",
            "ftp://u.shxj.pw",
        ]
        for url in test_cases:
            with self.subTest(url=url):
                self.assertTrue(is_link_shortener(url))

    def test_allowed_links(self) -> None:
        """Verify normal url strings are not flagged as blocked."""
        test_cases = [
            "http://google.com",
            "https://github.com/trending",
            "http://www.python.org",
            "http://subdomain.example.co.uk",
            "http://gu.to",
            "udp://www.gou.top",
            "smtp://gu.shxj.pw",
            "udp://gu.shxj.pw:2153",
            "ftp://gu.shxj.pw",
        ]
        for url in test_cases:
            with self.subTest(url=url):
                self.assertFalse(is_link_shortener(url))

    def test_invalid_type_raises_type_error(self) -> None:
        """Verify non-string arguments successfully raise a TypeError."""
        invalid_types = [
            None,
            123,
            ["https://bit.ly"],
            {"url": "t.co"},
        ]
        for invalid_input in invalid_types:
            with self.subTest(invalid_input=invalid_input):
                self.assertRaises(TypeError, is_link_shortener, invalid_input)

    def test_empty_or_blank_input_raises_value_error(self) -> None:
        """Verify empty and spacing strings raise a ValueError."""
        invalid_inputs = ["", "   ", "\n", "\t"]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                self.assertRaises(ValueError, is_link_shortener, invalid_input)

    def test_invalid_url_structures_raise_value_error(self) -> None:
        """Verify invalid url architectures raise a ValueError."""
        invalid_urls = [
            "just_some_text",
            "http://localhost",
            "www.ggaaa",
            "https://invalid",
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertRaises(ValueError, is_link_shortener, url)


if __name__ == "__main__":
    unittest.main()
