"""Financial ratio calculations — 30+ ratios across 5 categories."""

from __future__ import annotations

from dataclasses import dataclass

from fundx.analysis.common import safe_div
from fundx.data.models import BalanceSheet, CashFlowStatement, IncomeStatement, KeyMetrics


@dataclass
class ProfitabilityRatios:
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    ebitda_margin: float | None = None
    roa: float | None = None
    roe: float | None = None
    roic: float | None = None
    roce: float | None = None


@dataclass
class LiquidityRatios:
    current_ratio: float | None = None
    quick_ratio: float | None = None
    cash_ratio: float | None = None
    operating_cf_ratio: float | None = None


@dataclass
class SolvencyRatios:
    debt_to_equity: float | None = None
    debt_to_assets: float | None = None
    interest_coverage: float | None = None
    ebitda_interest_coverage: float | None = None
    net_debt_to_ebitda: float | None = None
    debt_to_fcf: float | None = None


@dataclass
class EfficiencyRatios:
    asset_turnover: float | None = None
    inventory_turnover: float | None = None
    receivable_turnover: float | None = None
    payable_turnover: float | None = None
    cash_conversion_cycle: float | None = None


@dataclass
class ValuationRatios:
    pe_ratio: float | None = None
    forward_pe: float | None = None
    pb_ratio: float | None = None
    ps_ratio: float | None = None
    p_to_fcf: float | None = None
    ev_to_ebitda: float | None = None
    ev_to_ebit: float | None = None
    peg_ratio: float | None = None
    earnings_yield: float | None = None
    dividend_yield: float | None = None
    fcf_yield: float | None = None


@dataclass
class AllRatios:
    period_end: str = ""
    profitability: ProfitabilityRatios | None = None
    liquidity: LiquidityRatios | None = None
    solvency: SolvencyRatios | None = None
    efficiency: EfficiencyRatios | None = None
    valuation: ValuationRatios | None = None


def calc_profitability(
    inc: IncomeStatement, bs: BalanceSheet
) -> ProfitabilityRatios:
    """Calculate profitability ratios from income statement and balance sheet."""
    total_debt = _total_debt(bs)
    invested_capital = _invested_capital(bs, total_debt)
    capital_employed = _capital_employed(bs)

    # NOPAT for ROIC
    nopat = None
    if inc.operating_income is not None and inc.income_tax_expense is not None and inc.income_before_tax is not None:
        tax_rate = safe_div(inc.income_tax_expense, inc.income_before_tax)
        if tax_rate is not None:
            nopat = inc.operating_income * (1 - tax_rate)

    return ProfitabilityRatios(
        gross_margin=safe_div(inc.gross_profit, inc.revenue),
        operating_margin=safe_div(inc.operating_income, inc.revenue),
        net_margin=safe_div(inc.net_income, inc.revenue),
        ebitda_margin=safe_div(inc.ebitda, inc.revenue),
        roa=safe_div(inc.net_income, bs.total_assets),
        roe=safe_div(inc.net_income, bs.total_stockholders_equity),
        roic=safe_div(nopat, invested_capital),
        roce=safe_div(inc.operating_income, capital_employed),
    )


def calc_liquidity(
    bs: BalanceSheet, cf: CashFlowStatement | None = None
) -> LiquidityRatios:
    """Calculate liquidity ratios."""
    quick_assets = None
    if bs.total_current_assets is not None and bs.inventory is not None:
        quick_assets = bs.total_current_assets - (bs.inventory or 0)

    return LiquidityRatios(
        current_ratio=safe_div(bs.total_current_assets, bs.total_current_liabilities),
        quick_ratio=safe_div(quick_assets, bs.total_current_liabilities),
        cash_ratio=safe_div(bs.cash_and_equivalents, bs.total_current_liabilities),
        operating_cf_ratio=safe_div(
            cf.operating_cash_flow if cf else None, bs.total_current_liabilities
        ),
    )


def calc_solvency(
    inc: IncomeStatement, bs: BalanceSheet, cf: CashFlowStatement | None = None
) -> SolvencyRatios:
    """Calculate solvency ratios."""
    total_debt = _total_debt(bs)
    net_debt = None
    if total_debt is not None and bs.cash_and_equivalents is not None:
        net_debt = total_debt - bs.cash_and_equivalents

    return SolvencyRatios(
        debt_to_equity=safe_div(total_debt, bs.total_stockholders_equity),
        debt_to_assets=safe_div(total_debt, bs.total_assets),
        interest_coverage=safe_div(
            inc.operating_income,
            abs(inc.interest_expense) if inc.interest_expense else None,
        ),
        ebitda_interest_coverage=safe_div(
            inc.ebitda,
            abs(inc.interest_expense) if inc.interest_expense else None,
        ),
        net_debt_to_ebitda=safe_div(net_debt, inc.ebitda),
        debt_to_fcf=safe_div(
            total_debt, cf.free_cash_flow if cf else None
        ),
    )


def calc_efficiency(
    inc: IncomeStatement, bs: BalanceSheet
) -> EfficiencyRatios:
    """Calculate efficiency ratios."""
    asset_turnover = safe_div(inc.revenue, bs.total_assets)
    inv_turnover = safe_div(inc.cost_of_revenue, bs.inventory)
    recv_turnover = safe_div(inc.revenue, bs.accounts_receivable)
    pay_turnover = safe_div(inc.cost_of_revenue, bs.accounts_payable)

    # Cash conversion cycle (in days)
    dio = safe_div(365.0, inv_turnover)
    dso = safe_div(365.0, recv_turnover)
    dpo = safe_div(365.0, pay_turnover)
    ccc = None
    if dio is not None and dso is not None and dpo is not None:
        ccc = dio + dso - dpo

    return EfficiencyRatios(
        asset_turnover=asset_turnover,
        inventory_turnover=inv_turnover,
        receivable_turnover=recv_turnover,
        payable_turnover=pay_turnover,
        cash_conversion_cycle=ccc,
    )


def calc_valuation(
    inc: IncomeStatement,
    bs: BalanceSheet,
    cf: CashFlowStatement | None,
    metrics: KeyMetrics | None,
) -> ValuationRatios:
    """Calculate valuation ratios."""
    market_cap = metrics.market_cap if metrics else None
    ev = metrics.enterprise_value if metrics else None

    fcf_yield = None
    if cf and cf.free_cash_flow and market_cap:
        fcf_yield = safe_div(cf.free_cash_flow, market_cap)

    p_to_fcf = None
    if cf and cf.free_cash_flow and market_cap:
        p_to_fcf = safe_div(market_cap, cf.free_cash_flow)

    earnings_yield = None
    if inc.net_income and market_cap:
        earnings_yield = safe_div(inc.net_income, market_cap)

    return ValuationRatios(
        pe_ratio=metrics.pe_ratio if metrics else None,
        forward_pe=metrics.forward_pe if metrics else None,
        pb_ratio=metrics.pb_ratio if metrics else None,
        ps_ratio=metrics.ps_ratio if metrics else None,
        p_to_fcf=p_to_fcf,
        ev_to_ebitda=metrics.ev_to_ebitda if metrics else safe_div(ev, inc.ebitda),
        ev_to_ebit=safe_div(ev, inc.operating_income),
        peg_ratio=None,  # Needs growth estimate — computed separately
        earnings_yield=earnings_yield,
        dividend_yield=metrics.dividend_yield if metrics else None,
        fcf_yield=fcf_yield,
    )


def calc_all_ratios(
    inc: IncomeStatement,
    bs: BalanceSheet,
    cf: CashFlowStatement | None = None,
    metrics: KeyMetrics | None = None,
) -> AllRatios:
    """Calculate all ratio categories for one period."""
    return AllRatios(
        period_end=str(inc.period_end),
        profitability=calc_profitability(inc, bs),
        liquidity=calc_liquidity(bs, cf),
        solvency=calc_solvency(inc, bs, cf),
        efficiency=calc_efficiency(inc, bs),
        valuation=calc_valuation(inc, bs, cf, metrics),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _total_debt(bs: BalanceSheet) -> float | None:
    short = bs.short_term_debt or 0
    long = bs.long_term_debt or 0
    if short == 0 and long == 0:
        return None
    return short + long


def _invested_capital(bs: BalanceSheet, total_debt: float | None) -> float | None:
    equity = bs.total_stockholders_equity
    if equity is None:
        return None
    cash = bs.cash_and_equivalents or 0
    debt = total_debt or 0
    return equity + debt - cash


def _capital_employed(bs: BalanceSheet) -> float | None:
    if bs.total_assets is None or bs.total_current_liabilities is None:
        return None
    return bs.total_assets - bs.total_current_liabilities
