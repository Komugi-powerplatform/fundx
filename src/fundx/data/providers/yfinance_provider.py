"""Yahoo Finance data provider adapter."""

from __future__ import annotations

from datetime import date

import yfinance as yf

from fundx.data.models import (
    BalanceSheet,
    CashFlowStatement,
    CompanyProfile,
    FinancialData,
    IncomeStatement,
    KeyMetrics,
)


def _pct_to_ratio(val: object) -> float | None:
    """Convert a percentage-form value to a decimal ratio.

    yfinance 1.2+ returns dividendYield in percentage form (e.g. 0.4 means
    0.4 %).  This helper divides by 100 so callers get a true ratio (0.004).
    """
    f = _safe(val)
    if f is None:
        return None
    # If value seems to be percentage form (> 0.01 = 1%), convert to ratio.
    # yfinance returns 0.4 for 0.4% yield, so divide by 100.
    return f / 100


def _safe(val: object) -> float | None:
    """Safely convert a value to float, returning None for NaN/None."""
    if val is None:
        return None
    try:
        f = float(val)
        if f != f:  # NaN check
            return None
        return f
    except (ValueError, TypeError):
        return None


def _parse_date(idx: object) -> date:
    """Parse a pandas Timestamp index to a date."""
    import pandas as pd

    if isinstance(idx, pd.Timestamp):
        return idx.date()
    return date.today()


class YFinanceProvider:
    """Adapter for yfinance library."""

    def __init__(self) -> None:
        self._tickers: dict[str, yf.Ticker] = {}

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        """Return a cached ``yf.Ticker`` instance for *symbol*."""
        if symbol not in self._tickers:
            self._tickers[symbol] = yf.Ticker(symbol)
        return self._tickers[symbol]

    def get_company_profile(self, ticker: str) -> CompanyProfile:
        t = self._get_ticker(ticker)
        info = t.info
        return CompanyProfile(
            ticker=ticker,
            name=info.get("longName") or info.get("shortName") or ticker,
            exchange=info.get("exchange", ""),
            currency=info.get("currency", "USD"),
            sector=info.get("sector", ""),
            industry=info.get("industry", ""),
            market_cap=_safe(info.get("marketCap")),
            description=info.get("longBusinessSummary", ""),
            country=info.get("country", ""),
            website=info.get("website", ""),
        )

    def get_income_statements(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[IncomeStatement]:
        t = self._get_ticker(ticker)
        if period == "quarterly":
            df = t.quarterly_income_stmt
        else:
            df = t.income_stmt

        if df is None or df.empty:
            return []

        results: list[IncomeStatement] = []
        for col in list(df.columns)[:limit]:
            s = df[col]
            results.append(
                IncomeStatement(
                    period_end=_parse_date(col),
                    period_type=period,
                    revenue=_safe(s.get("Total Revenue")),
                    cost_of_revenue=_safe(s.get("Cost Of Revenue")),
                    gross_profit=_safe(s.get("Gross Profit")),
                    research_and_development=_safe(s.get("Research And Development")),
                    selling_general_admin=_safe(
                        s.get("Selling General And Administration")
                    ),
                    operating_expenses=_safe(s.get("Total Operating Expenses") or s.get("Operating Expense")),
                    operating_income=_safe(s.get("Operating Income")),
                    interest_expense=_safe(s.get("Interest Expense")),
                    other_income=_safe(s.get("Other Income Expense")),
                    income_before_tax=_safe(s.get("Pretax Income")),
                    income_tax_expense=_safe(s.get("Tax Provision")),
                    net_income=_safe(s.get("Net Income")),
                    ebitda=_safe(s.get("EBITDA")),
                    eps_basic=_safe(s.get("Basic EPS")),
                    eps_diluted=_safe(s.get("Diluted EPS")),
                    shares_outstanding=_safe(s.get("Basic Average Shares")),
                    shares_diluted=_safe(s.get("Diluted Average Shares")),
                )
            )
        return results

    def get_balance_sheets(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[BalanceSheet]:
        t = self._get_ticker(ticker)
        if period == "quarterly":
            df = t.quarterly_balance_sheet
        else:
            df = t.balance_sheet

        if df is None or df.empty:
            return []

        results: list[BalanceSheet] = []
        for col in list(df.columns)[:limit]:
            s = df[col]
            results.append(
                BalanceSheet(
                    period_end=_parse_date(col),
                    period_type=period,
                    cash_and_equivalents=_safe(
                        s.get("Cash And Cash Equivalents")
                    ),
                    short_term_investments=_safe(
                        s.get("Other Short Term Investments")
                    ),
                    accounts_receivable=_safe(s.get("Accounts Receivable")),
                    inventory=_safe(s.get("Inventory")),
                    other_current_assets=_safe(s.get("Other Current Assets")),
                    total_current_assets=_safe(s.get("Current Assets")),
                    property_plant_equipment=_safe(
                        s.get("Net PPE") or s.get("Property Plant Equipment Net")
                    ),
                    goodwill=_safe(s.get("Goodwill")),
                    intangible_assets=_safe(s.get("Other Intangible Assets")),
                    other_non_current_assets=_safe(
                        s.get("Other Non Current Assets")
                    ),
                    total_non_current_assets=_safe(
                        s.get("Total Non Current Assets")
                    ),
                    total_assets=_safe(s.get("Total Assets")),
                    accounts_payable=_safe(s.get("Accounts Payable")),
                    short_term_debt=_safe(
                        s.get("Current Debt") or s.get("Short Term Borrowings")
                    ),
                    current_portion_long_term_debt=_safe(
                        s.get("Current Debt And Capital Lease Obligation")
                    ),
                    other_current_liabilities=_safe(
                        s.get("Other Current Liabilities")
                    ),
                    total_current_liabilities=_safe(
                        s.get("Current Liabilities")
                    ),
                    long_term_debt=_safe(s.get("Long Term Debt")),
                    other_non_current_liabilities=_safe(
                        s.get("Other Non Current Liabilities")
                    ),
                    total_non_current_liabilities=_safe(
                        s.get("Total Non Current Liabilities Net Minority Interest")
                    ),
                    total_liabilities=_safe(
                        s.get("Total Liabilities Net Minority Interest")
                    ),
                    common_stock=_safe(s.get("Common Stock")),
                    retained_earnings=_safe(s.get("Retained Earnings")),
                    total_stockholders_equity=_safe(
                        s.get("Stockholders Equity")
                        or s.get("Total Equity Gross Minority Interest")
                    ),
                )
            )
        return results

    def get_cash_flows(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> list[CashFlowStatement]:
        t = self._get_ticker(ticker)
        if period == "quarterly":
            df = t.quarterly_cashflow
        else:
            df = t.cashflow

        if df is None or df.empty:
            return []

        results: list[CashFlowStatement] = []
        for col in list(df.columns)[:limit]:
            s = df[col]
            capex = _safe(s.get("Capital Expenditure"))
            ocf = _safe(s.get("Operating Cash Flow"))
            fcf = None
            if ocf is not None and capex is not None:
                fcf = ocf + capex  # capex is typically negative

            results.append(
                CashFlowStatement(
                    period_end=_parse_date(col),
                    period_type=period,
                    net_income=_safe(s.get("Net Income")),
                    depreciation_amortization=_safe(
                        s.get("Depreciation And Amortization")
                    ),
                    stock_based_compensation=_safe(
                        s.get("Stock Based Compensation")
                    ),
                    change_in_working_capital=_safe(
                        s.get("Change In Working Capital")
                    ),
                    operating_cash_flow=ocf,
                    capital_expenditure=capex,
                    acquisitions=_safe(
                        s.get("Acquisitions And Disposals")
                    ),
                    investment_purchases=_safe(
                        s.get("Purchase Of Investment")
                    ),
                    investment_sales=_safe(s.get("Sale Of Investment")),
                    investing_cash_flow=_safe(s.get("Investing Cash Flow")),
                    debt_issuance=_safe(s.get("Issuance Of Debt")),
                    debt_repayment=_safe(s.get("Repayment Of Debt")),
                    share_repurchase=_safe(
                        s.get("Repurchase Of Capital Stock")
                    ),
                    dividends_paid=_safe(
                        s.get("Common Stock Dividend Paid")
                        or s.get("Cash Dividends Paid")
                    ),
                    financing_cash_flow=_safe(s.get("Financing Cash Flow")),
                    free_cash_flow=_safe(s.get("Free Cash Flow")) or fcf,
                )
            )
        return results

    def get_key_metrics(self, ticker: str) -> KeyMetrics:
        t = self._get_ticker(ticker)
        info = t.info
        return KeyMetrics(
            ticker=ticker,
            price=_safe(info.get("currentPrice") or info.get("regularMarketPrice")),
            market_cap=_safe(info.get("marketCap")),
            enterprise_value=_safe(info.get("enterpriseValue")),
            pe_ratio=_safe(info.get("trailingPE")),
            forward_pe=_safe(info.get("forwardPE")),
            pb_ratio=_safe(info.get("priceToBook")),
            ps_ratio=_safe(info.get("priceToSalesTrailing12Months")),
            ev_to_ebitda=_safe(info.get("enterpriseToEbitda")),
            dividend_yield=_pct_to_ratio(info.get("dividendYield")),
            beta=_safe(info.get("beta")),
            fifty_two_week_high=_safe(info.get("fiftyTwoWeekHigh")),
            fifty_two_week_low=_safe(info.get("fiftyTwoWeekLow")),
        )

    def get_financial_data(
        self, ticker: str, period: str = "annual", limit: int = 5
    ) -> FinancialData:
        """Fetch all financial data for a ticker in one call."""
        return FinancialData(
            profile=self.get_company_profile(ticker),
            income_statements=self.get_income_statements(ticker, period, limit),
            balance_sheets=self.get_balance_sheets(ticker, period, limit),
            cash_flows=self.get_cash_flows(ticker, period, limit),
            metrics=self.get_key_metrics(ticker),
        )

    def search_ticker(self, query: str) -> list[dict[str, str]]:
        """Search for tickers by company name."""
        try:
            results = yf.Search(query)
            quotes = results.quotes if hasattr(results, "quotes") else []
            return [
                {
                    "ticker": q.get("symbol", ""),
                    "name": q.get("longname") or q.get("shortname", ""),
                    "exchange": q.get("exchDisp") or q.get("exchange", ""),
                    "type": q.get("quoteType", ""),
                }
                for q in quotes
                if q.get("quoteType") == "EQUITY"
            ]
        except Exception:
            return []
