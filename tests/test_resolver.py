"""Tests for fundx.data.resolver — ticker resolution logic."""

from fundx.data.resolver import _looks_like_ticker


class TestLooksLikeTicker:
    def test_simple_ticker(self):
        assert _looks_like_ticker("AAPL") is True

    def test_short_ticker(self):
        assert _looks_like_ticker("A") is True

    def test_numeric_ticker(self):
        assert _looks_like_ticker("7203") is True

    def test_japanese_ticker(self):
        assert _looks_like_ticker("7203.T") is True

    def test_london_ticker(self):
        assert _looks_like_ticker("SHEL.L") is True

    def test_lowercase_converted(self):
        assert _looks_like_ticker("aapl") is True

    def test_too_long(self):
        assert _looks_like_ticker("ABCDEF") is False

    def test_company_name(self):
        assert _looks_like_ticker("Apple Inc") is False

    def test_with_special_chars(self):
        assert _looks_like_ticker("AA-PL") is False

    def test_empty(self):
        assert _looks_like_ticker("") is False
