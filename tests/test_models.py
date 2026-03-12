"""Tests for fundx.data.models — Pydantic model validation."""

from datetime import date

from fundx.data.models import (
    BalanceSheet,
    CashFlowStatement,
    CompanyProfile,
    FinancialData,
    IncomeStatement,
    KeyMetrics,
)


class TestIncomeStatement:
    def test_minimal(self):
        s = IncomeStatement(period_end=date(2024, 12, 31))
        assert s.revenue is None
        assert s.period_type == "annual"

    def test_full(self):
        s = IncomeStatement(
            period_end=date(2024, 12, 31),
            period_type="quarterly",
            revenue=1_000_000,
            net_income=100_000,
        )
        assert s.revenue == 1_000_000
        assert s.period_type == "quarterly"


class TestBalanceSheet:
    def test_minimal(self):
        bs = BalanceSheet(period_end=date(2024, 12, 31))
        assert bs.total_assets is None

    def test_equity_calculation(self):
        bs = BalanceSheet(
            period_end=date(2024, 12, 31),
            total_assets=1_000_000,
            total_liabilities=400_000,
            total_stockholders_equity=600_000,
        )
        assert bs.total_assets - bs.total_liabilities == bs.total_stockholders_equity


class TestCashFlowStatement:
    def test_free_cash_flow(self):
        cf = CashFlowStatement(
            period_end=date(2024, 12, 31),
            operating_cash_flow=200_000,
            capital_expenditure=-50_000,
            free_cash_flow=150_000,
        )
        assert cf.free_cash_flow == 150_000


class TestCompanyProfile:
    def test_defaults(self):
        p = CompanyProfile(ticker="AAPL", name="Apple Inc.")
        assert p.currency == "USD"
        assert p.sector == ""

    def test_full(self):
        p = CompanyProfile(
            ticker="AAPL",
            name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=3e12,
        )
        assert p.market_cap == 3e12


class TestKeyMetrics:
    def test_minimal(self):
        m = KeyMetrics(ticker="AAPL")
        assert m.price is None
        assert m.pe_ratio is None

    def test_with_values(self):
        m = KeyMetrics(ticker="AAPL", price=150.0, pe_ratio=25.0)
        assert m.price == 150.0


class TestFinancialData:
    def test_empty(self):
        fd = FinancialData(
            profile=CompanyProfile(ticker="TEST", name="Test Co"),
        )
        assert fd.income_statements == []
        assert fd.metrics is None
