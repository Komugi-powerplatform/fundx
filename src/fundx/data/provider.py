"""Abstract data provider protocol."""

from __future__ import annotations

from typing import Protocol

from fundx.data.models import (
    BalanceSheet,
    CashFlowStatement,
    CompanyProfile,
    FinancialData,
    IncomeStatement,
    KeyMetrics,
)


class DataProvider(Protocol):
    """Interface that all data source adapters must implement."""

    def get_company_profile(self, ticker: str) -> CompanyProfile: ...

    def get_income_statements(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[IncomeStatement]: ...

    def get_balance_sheets(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[BalanceSheet]: ...

    def get_cash_flows(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[CashFlowStatement]: ...

    def get_key_metrics(self, ticker: str) -> KeyMetrics: ...

    def get_financial_data(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> FinancialData: ...

    def search_ticker(self, query: str) -> list[dict[str, str]]:
        """Search for tickers by company name. Returns list of {ticker, name, exchange}."""
        ...
