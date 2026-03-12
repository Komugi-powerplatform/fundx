"""Tests for fundx.analysis.ratios — financial ratio calculations."""

from datetime import date

from fundx.analysis.ratios import (
    AllRatios,
    calc_all_ratios,
    calc_efficiency,
    calc_liquidity,
    calc_profitability,
    calc_solvency,
    calc_valuation,
)
from fundx.data.models import BalanceSheet, CashFlowStatement, IncomeStatement, KeyMetrics


def _make_income(**overrides) -> IncomeStatement:
    defaults = dict(
        period_end=date(2024, 12, 31),
        revenue=1_000_000,
        cost_of_revenue=600_000,
        gross_profit=400_000,
        operating_income=200_000,
        operating_expenses=800_000,
        interest_expense=-20_000,
        income_before_tax=180_000,
        income_tax_expense=36_000,
        net_income=144_000,
        ebitda=250_000,
        eps_diluted=2.88,
        shares_diluted=50_000,
    )
    defaults.update(overrides)
    return IncomeStatement(**defaults)


def _make_balance(**overrides) -> BalanceSheet:
    defaults = dict(
        period_end=date(2024, 12, 31),
        cash_and_equivalents=100_000,
        accounts_receivable=80_000,
        inventory=60_000,
        total_current_assets=300_000,
        total_current_liabilities=200_000,
        total_assets=1_000_000,
        short_term_debt=50_000,
        long_term_debt=150_000,
        total_liabilities=400_000,
        total_stockholders_equity=600_000,
        accounts_payable=70_000,
        retained_earnings=500_000,
    )
    defaults.update(overrides)
    return BalanceSheet(**defaults)


def _make_cashflow(**overrides) -> CashFlowStatement:
    defaults = dict(
        period_end=date(2024, 12, 31),
        operating_cash_flow=220_000,
        capital_expenditure=-50_000,
        free_cash_flow=170_000,
        net_income=144_000,
    )
    defaults.update(overrides)
    return CashFlowStatement(**defaults)


def _make_metrics(**overrides) -> KeyMetrics:
    defaults = dict(
        ticker="TEST",
        price=100.0,
        market_cap=5_000_000,
        enterprise_value=5_100_000,
        pe_ratio=34.7,
        forward_pe=28.0,
        pb_ratio=8.3,
        ps_ratio=5.0,
        ev_to_ebitda=20.4,
        dividend_yield=0.005,
        beta=1.2,
    )
    defaults.update(overrides)
    return KeyMetrics(**defaults)


class TestProfitability:
    def test_margins(self):
        r = calc_profitability(_make_income(), _make_balance())
        assert r.gross_margin is not None
        assert abs(r.gross_margin - 0.40) < 1e-6
        assert r.operating_margin is not None
        assert abs(r.operating_margin - 0.20) < 1e-6
        assert r.net_margin is not None
        assert abs(r.net_margin - 0.144) < 1e-6

    def test_roe_roa(self):
        r = calc_profitability(_make_income(), _make_balance())
        # ROA = 144k / 1M = 0.144
        assert r.roa is not None
        assert abs(r.roa - 0.144) < 1e-6
        # ROE = 144k / 600k = 0.24
        assert r.roe is not None
        assert abs(r.roe - 0.24) < 1e-6

    def test_roic(self):
        r = calc_profitability(_make_income(), _make_balance())
        # tax_rate = 36k / 180k = 0.2
        # NOPAT = 200k * (1 - 0.2) = 160k
        # invested_capital = 600k + 200k - 100k = 700k
        # ROIC = 160k / 700k ≈ 0.2286
        assert r.roic is not None
        assert abs(r.roic - 160_000 / 700_000) < 1e-6

    def test_none_revenue(self):
        r = calc_profitability(_make_income(revenue=None), _make_balance())
        assert r.gross_margin is None
        assert r.operating_margin is None
        assert r.net_margin is None


class TestLiquidity:
    def test_current_ratio(self):
        r = calc_liquidity(_make_balance())
        # 300k / 200k = 1.5
        assert r.current_ratio is not None
        assert abs(r.current_ratio - 1.5) < 1e-6

    def test_quick_ratio(self):
        r = calc_liquidity(_make_balance())
        # (300k - 60k) / 200k = 1.2
        assert r.quick_ratio is not None
        assert abs(r.quick_ratio - 1.2) < 1e-6

    def test_cash_ratio(self):
        r = calc_liquidity(_make_balance())
        # 100k / 200k = 0.5
        assert r.cash_ratio is not None
        assert abs(r.cash_ratio - 0.5) < 1e-6

    def test_operating_cf_ratio(self):
        r = calc_liquidity(_make_balance(), _make_cashflow())
        # 220k / 200k = 1.1
        assert r.operating_cf_ratio is not None
        assert abs(r.operating_cf_ratio - 1.1) < 1e-6

    def test_without_cashflow(self):
        r = calc_liquidity(_make_balance())
        assert r.operating_cf_ratio is None


class TestSolvency:
    def test_debt_to_equity(self):
        r = calc_solvency(_make_income(), _make_balance())
        # total_debt = 50k + 150k = 200k, equity = 600k
        assert r.debt_to_equity is not None
        assert abs(r.debt_to_equity - 200_000 / 600_000) < 1e-6

    def test_interest_coverage(self):
        r = calc_solvency(_make_income(), _make_balance())
        # operating_income / |interest_expense| = 200k / 20k = 10
        assert r.interest_coverage is not None
        assert abs(r.interest_coverage - 10.0) < 1e-6

    def test_net_debt_to_ebitda(self):
        r = calc_solvency(_make_income(), _make_balance())
        # net_debt = 200k - 100k = 100k, EBITDA = 250k
        assert r.net_debt_to_ebitda is not None
        assert abs(r.net_debt_to_ebitda - 100_000 / 250_000) < 1e-6

    def test_no_debt(self):
        r = calc_solvency(
            _make_income(),
            _make_balance(short_term_debt=0, long_term_debt=0),
        )
        assert r.debt_to_equity is None


class TestEfficiency:
    def test_asset_turnover(self):
        r = calc_efficiency(_make_income(), _make_balance())
        # 1M / 1M = 1.0
        assert r.asset_turnover is not None
        assert abs(r.asset_turnover - 1.0) < 1e-6

    def test_inventory_turnover(self):
        r = calc_efficiency(_make_income(), _make_balance())
        # 600k / 60k = 10.0
        assert r.inventory_turnover is not None
        assert abs(r.inventory_turnover - 10.0) < 1e-6

    def test_cash_conversion_cycle(self):
        r = calc_efficiency(_make_income(), _make_balance())
        # DIO = 365/10 = 36.5, DSO = 365/12.5 = 29.2, DPO = 365/8.57 ≈ 42.6
        # CCC = 36.5 + 29.2 - 42.6 ≈ 23.1
        assert r.cash_conversion_cycle is not None
        assert 20 < r.cash_conversion_cycle < 30

    def test_no_inventory(self):
        r = calc_efficiency(_make_income(), _make_balance(inventory=None))
        assert r.inventory_turnover is None


class TestValuation:
    def test_pe_from_metrics(self):
        r = calc_valuation(_make_income(), _make_balance(), _make_cashflow(), _make_metrics())
        assert r.pe_ratio == 34.7
        assert r.forward_pe == 28.0

    def test_fcf_yield(self):
        r = calc_valuation(_make_income(), _make_balance(), _make_cashflow(), _make_metrics())
        # FCF 170k / market_cap 5M = 0.034
        assert r.fcf_yield is not None
        assert abs(r.fcf_yield - 170_000 / 5_000_000) < 1e-6

    def test_earnings_yield(self):
        r = calc_valuation(_make_income(), _make_balance(), _make_cashflow(), _make_metrics())
        # 144k / 5M = 0.0288
        assert r.earnings_yield is not None
        assert abs(r.earnings_yield - 144_000 / 5_000_000) < 1e-6

    def test_without_metrics(self):
        r = calc_valuation(_make_income(), _make_balance(), _make_cashflow(), None)
        assert r.pe_ratio is None
        assert r.forward_pe is None


class TestCalcAllRatios:
    def test_returns_all_categories(self):
        r = calc_all_ratios(_make_income(), _make_balance(), _make_cashflow(), _make_metrics())
        assert isinstance(r, AllRatios)
        assert r.profitability is not None
        assert r.liquidity is not None
        assert r.solvency is not None
        assert r.efficiency is not None
        assert r.valuation is not None
        assert r.period_end == "2024-12-31"

    def test_minimal_data(self):
        inc = IncomeStatement(period_end=date(2024, 12, 31))
        bs = BalanceSheet(period_end=date(2024, 12, 31))
        r = calc_all_ratios(inc, bs)
        assert r.profitability is not None
        assert r.profitability.gross_margin is None
