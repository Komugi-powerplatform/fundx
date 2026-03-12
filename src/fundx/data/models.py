"""Pydantic models for normalized financial data."""

from __future__ import annotations

from datetime import date
from pydantic import BaseModel


class CompanyProfile(BaseModel):
    """Basic company information."""

    ticker: str
    name: str
    exchange: str = ""
    currency: str = "USD"
    sector: str = ""
    industry: str = ""
    market_cap: float | None = None
    description: str = ""
    country: str = ""
    website: str = ""


class IncomeStatement(BaseModel):
    """Standardized income statement line items."""

    period_end: date
    period_type: str = "annual"  # "annual" or "quarterly"

    # Revenue
    revenue: float | None = None
    cost_of_revenue: float | None = None
    gross_profit: float | None = None

    # Operating
    research_and_development: float | None = None
    selling_general_admin: float | None = None
    operating_expenses: float | None = None
    operating_income: float | None = None

    # Non-operating
    interest_expense: float | None = None
    other_income: float | None = None
    income_before_tax: float | None = None
    income_tax_expense: float | None = None

    # Bottom line
    net_income: float | None = None
    ebitda: float | None = None
    eps_basic: float | None = None
    eps_diluted: float | None = None
    shares_outstanding: float | None = None
    shares_diluted: float | None = None


class BalanceSheet(BaseModel):
    """Standardized balance sheet line items."""

    period_end: date
    period_type: str = "annual"

    # Current assets
    cash_and_equivalents: float | None = None
    short_term_investments: float | None = None
    accounts_receivable: float | None = None
    inventory: float | None = None
    other_current_assets: float | None = None
    total_current_assets: float | None = None

    # Non-current assets
    property_plant_equipment: float | None = None
    goodwill: float | None = None
    intangible_assets: float | None = None
    other_non_current_assets: float | None = None
    total_non_current_assets: float | None = None
    total_assets: float | None = None

    # Current liabilities
    accounts_payable: float | None = None
    short_term_debt: float | None = None
    current_portion_long_term_debt: float | None = None
    other_current_liabilities: float | None = None
    total_current_liabilities: float | None = None

    # Non-current liabilities
    long_term_debt: float | None = None
    other_non_current_liabilities: float | None = None
    total_non_current_liabilities: float | None = None
    total_liabilities: float | None = None

    # Equity
    common_stock: float | None = None
    retained_earnings: float | None = None
    total_stockholders_equity: float | None = None


class CashFlowStatement(BaseModel):
    """Standardized cash flow statement line items."""

    period_end: date
    period_type: str = "annual"

    # Operating
    net_income: float | None = None
    depreciation_amortization: float | None = None
    stock_based_compensation: float | None = None
    change_in_working_capital: float | None = None
    operating_cash_flow: float | None = None

    # Investing
    capital_expenditure: float | None = None
    acquisitions: float | None = None
    investment_purchases: float | None = None
    investment_sales: float | None = None
    investing_cash_flow: float | None = None

    # Financing
    debt_issuance: float | None = None
    debt_repayment: float | None = None
    share_repurchase: float | None = None
    dividends_paid: float | None = None
    financing_cash_flow: float | None = None

    # Derived
    free_cash_flow: float | None = None


class KeyMetrics(BaseModel):
    """Current market and valuation metrics."""

    ticker: str
    price: float | None = None
    market_cap: float | None = None
    enterprise_value: float | None = None
    pe_ratio: float | None = None
    forward_pe: float | None = None
    pb_ratio: float | None = None
    ps_ratio: float | None = None
    ev_to_ebitda: float | None = None
    dividend_yield: float | None = None
    beta: float | None = None
    fifty_two_week_high: float | None = None
    fifty_two_week_low: float | None = None


class FinancialData(BaseModel):
    """Complete financial dataset for a company."""

    profile: CompanyProfile
    income_statements: list[IncomeStatement] = []
    balance_sheets: list[BalanceSheet] = []
    cash_flows: list[CashFlowStatement] = []
    metrics: KeyMetrics | None = None
