"""Tests for fundx.analysis.common — math utilities."""

from fundx.analysis.common import cagr, safe_div, safe_pct, yoy_growth


class TestSafeDiv:
    def test_normal(self):
        assert safe_div(10, 2) == 5.0

    def test_zero_denominator(self):
        assert safe_div(10, 0) is None

    def test_none_numerator(self):
        assert safe_div(None, 2) is None

    def test_none_denominator(self):
        assert safe_div(10, None) is None

    def test_both_none(self):
        assert safe_div(None, None) is None

    def test_negative(self):
        assert safe_div(-10, 2) == -5.0

    def test_float_precision(self):
        result = safe_div(1, 3)
        assert result is not None
        assert abs(result - 0.3333333) < 1e-5


class TestSafePct:
    def test_normal(self):
        assert safe_pct(0.15) == 15.0

    def test_none(self):
        assert safe_pct(None) is None

    def test_zero(self):
        assert safe_pct(0) == 0.0

    def test_negative(self):
        assert safe_pct(-0.05) == -5.0


class TestCagr:
    def test_normal(self):
        # 100 -> 200 in 3 years ≈ 26%
        result = cagr(100, 200, 3)
        assert result is not None
        assert abs(result - 0.2599) < 0.01

    def test_no_growth(self):
        result = cagr(100, 100, 5)
        assert result is not None
        assert abs(result) < 1e-10

    def test_negative_begin(self):
        assert cagr(-100, 200, 3) is None

    def test_negative_end(self):
        assert cagr(100, -200, 3) is None

    def test_zero_years(self):
        assert cagr(100, 200, 0) is None

    def test_none_inputs(self):
        assert cagr(None, 200, 3) is None
        assert cagr(100, None, 3) is None


class TestYoyGrowth:
    def test_positive_growth(self):
        result = yoy_growth(120, 100)
        assert result is not None
        assert abs(result - 0.20) < 1e-10

    def test_negative_growth(self):
        result = yoy_growth(80, 100)
        assert result is not None
        assert abs(result - (-0.20)) < 1e-10

    def test_zero_previous(self):
        assert yoy_growth(100, 0) is None

    def test_none_inputs(self):
        assert yoy_growth(None, 100) is None
        assert yoy_growth(100, None) is None

    def test_from_negative_previous(self):
        # -100 to 50: (50 - (-100)) / |-100| = 1.5
        result = yoy_growth(50, -100)
        assert result is not None
        assert abs(result - 1.5) < 1e-10
