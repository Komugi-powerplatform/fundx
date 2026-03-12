"""Tests for fundx.cli.formatters — number formatting and color logic."""

from fundx.cli.formatters.colors import fmt_colored_ratio, fmt_number, fmt_ratio, signal_color


class TestFmtNumber:
    def test_none(self):
        assert fmt_number(None) == "[dim]—[/dim]"

    def test_trillion(self):
        assert fmt_number(2.5e12) == "2.50T"

    def test_billion(self):
        assert fmt_number(1.23e9) == "1.23B"

    def test_million(self):
        assert fmt_number(45.6e6) == "45.60M"

    def test_thousand(self):
        assert fmt_number(7800) == "7.80K"

    def test_small(self):
        assert fmt_number(42.5) == "42.50"

    def test_negative_billion(self):
        assert fmt_number(-3.2e9) == "-3.20B"

    def test_percent(self):
        assert fmt_number(0.15, pct=True) == "15.00%"

    def test_custom_decimals(self):
        assert fmt_number(1.23456e9, decimals=1) == "1.2B"

    def test_zero(self):
        assert fmt_number(0) == "0.00"


class TestFmtRatio:
    def test_none(self):
        assert fmt_ratio(None) == "[dim]—[/dim]"

    def test_normal(self):
        assert fmt_ratio(1.5) == "1.50"

    def test_custom_decimals(self):
        assert fmt_ratio(0.12345, decimals=3) == "0.123"


class TestSignalColor:
    def test_none_value(self):
        assert signal_color("roe", None) == "dim"

    def test_unknown_metric(self):
        assert signal_color("nonexistent", 1.0) == "white"

    def test_roe_good(self):
        # good threshold = 0.15
        assert signal_color("roe", 0.20) == "green"

    def test_roe_warning(self):
        # warning threshold = 0.08
        assert signal_color("roe", 0.10) == "yellow"

    def test_roe_bad(self):
        assert signal_color("roe", 0.02) == "red"

    def test_debt_to_equity_good(self):
        # good=1.0 (lower is better), warning=2.0
        assert signal_color("debt_to_equity", 0.5) == "green"

    def test_debt_to_equity_warning(self):
        assert signal_color("debt_to_equity", 1.5) == "yellow"

    def test_debt_to_equity_bad(self):
        assert signal_color("debt_to_equity", 3.0) == "red"


class TestFmtColoredRatio:
    def test_none(self):
        assert fmt_colored_ratio("roe", None) == "[dim]—[/dim]"

    def test_good_pct(self):
        result = fmt_colored_ratio("roe", 0.20, pct=True)
        assert "[green]" in result
        assert "20.00%" in result

    def test_bad_no_pct(self):
        result = fmt_colored_ratio("debt_to_equity", 3.0, pct=False)
        assert "[red]" in result
        assert "3.00" in result
