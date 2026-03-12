"""Tests for fundx.analysis.builder."""

from datetime import date

from fundx.analysis.builder import build_ratios_list
from fundx.data.models import BalanceSheet, CashFlowStatement, IncomeStatement, KeyMetrics


def _inc(d: date) -> IncomeStatement:
    return IncomeStatement(period_end=d, revenue=1_000_000, net_income=100_000,
                           gross_profit=400_000, operating_income=200_000,
                           income_before_tax=180_000, income_tax_expense=36_000)


def _bs(d: date) -> BalanceSheet:
    return BalanceSheet(period_end=d, total_assets=1_000_000,
                        total_stockholders_equity=600_000,
                        total_current_assets=300_000,
                        total_current_liabilities=200_000)


def _cf(d: date) -> CashFlowStatement:
    return CashFlowStatement(period_end=d, operating_cash_flow=220_000,
                              free_cash_flow=170_000)


class TestBuildRatiosList:
    def test_basic(self):
        dates = [date(2024, 12, 31), date(2023, 12, 31)]
        result = build_ratios_list(
            [_inc(d) for d in dates],
            [_bs(d) for d in dates],
            [_cf(d) for d in dates],
        )
        assert len(result) == 2
        assert result[0].period_end == "2024-12-31"
        assert result[1].period_end == "2023-12-31"

    def test_metrics_only_on_latest(self):
        dates = [date(2024, 12, 31), date(2023, 12, 31)]
        metrics = KeyMetrics(ticker="TEST", pe_ratio=25.0)
        result = build_ratios_list(
            [_inc(d) for d in dates],
            [_bs(d) for d in dates],
            [_cf(d) for d in dates],
            metrics,
        )
        assert result[0].valuation is not None
        assert result[0].valuation.pe_ratio == 25.0
        assert result[1].valuation is not None
        assert result[1].valuation.pe_ratio is None

    def test_mismatched_lengths(self):
        result = build_ratios_list(
            [_inc(date(2024, 12, 31)), _inc(date(2023, 12, 31))],
            [_bs(date(2024, 12, 31))],
            [],
        )
        assert len(result) == 1

    def test_empty_lists(self):
        result = build_ratios_list([], [], [])
        assert result == []

    def test_fewer_cashflows(self):
        dates = [date(2024, 12, 31), date(2023, 12, 31)]
        result = build_ratios_list(
            [_inc(d) for d in dates],
            [_bs(d) for d in dates],
            [_cf(dates[0])],  # only 1 CF
        )
        assert len(result) == 2
        assert result[0].liquidity is not None
        assert result[0].liquidity.operating_cf_ratio is not None
        assert result[1].liquidity is not None
        assert result[1].liquidity.operating_cf_ratio is None
