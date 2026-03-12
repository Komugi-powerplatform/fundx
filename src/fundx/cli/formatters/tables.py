"""Rich table builders for financial data display."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from fundx.analysis.ratios import AllRatios
from fundx.cli.formatters.colors import fmt_colored_ratio
from fundx.cli.formatters.fmt import fmt_number
from fundx.data.models import (
    BalanceSheet,
    CashFlowStatement,
    CompanyProfile,
    IncomeStatement,
    KeyMetrics,
)

console = Console()


def _print_statement_table(
    title: str,
    items: list,
    rows: list[tuple[str, str | None]],
) -> None:
    """Generic financial statement table printer.

    Each row is (label, field_name). If field_name is None, an empty separator row is added.
    """
    if not items:
        console.print(f"[dim]No {title.lower()} data available.[/dim]")
        return

    table = Table(title=title, show_lines=True, title_style="bold")
    table.add_column("Item", style="bold", min_width=25)
    for item in items:
        table.add_column(str(item.period_end), justify="right", min_width=12)

    for label, field in rows:
        if field is None:
            table.add_row("")
            continue
        values = [fmt_number(getattr(item, field)) for item in items]
        table.add_row(label, *values)

    console.print(table)


def print_profile(profile: CompanyProfile, metrics: KeyMetrics | None = None) -> None:
    """Display company profile header."""
    lines = [
        f"[bold cyan]{profile.name}[/bold cyan]  [dim]({profile.ticker})[/dim]",
        f"Sector: {profile.sector or '—'}  |  Industry: {profile.industry or '—'}",
        f"Exchange: {profile.exchange or '—'}  |  Currency: {profile.currency}  |  Country: {profile.country or '—'}",
    ]
    if metrics:
        price_str = fmt_number(metrics.price, decimals=2)
        mcap_str = fmt_number(metrics.market_cap)
        ev_str = fmt_number(metrics.enterprise_value)
        lines.append(f"Price: {price_str}  |  Market Cap: {mcap_str}  |  EV: {ev_str}")
        if metrics.fifty_two_week_low and metrics.fifty_two_week_high:
            lines.append(
                f"52W Range: {fmt_number(metrics.fifty_two_week_low, 2)} — {fmt_number(metrics.fifty_two_week_high, 2)}"
                f"  |  Beta: {fmt_number(metrics.beta, 2)}"
            )
    console.print(Panel("\n".join(lines), title="Company Overview", border_style="blue"))


def print_income_statements(statements: list[IncomeStatement]) -> None:
    """Display income statements as a table."""
    rows = [
        ("Revenue", "revenue"),
        ("Cost of Revenue", "cost_of_revenue"),
        ("Gross Profit", "gross_profit"),
        ("R&D", "research_and_development"),
        ("SG&A", "selling_general_admin"),
        ("Operating Income", "operating_income"),
        ("Interest Expense", "interest_expense"),
        ("Income Before Tax", "income_before_tax"),
        ("Tax Expense", "income_tax_expense"),
        ("Net Income", "net_income"),
        ("EBITDA", "ebitda"),
        ("EPS (Diluted)", "eps_diluted"),
    ]
    _print_statement_table("Income Statement", statements, rows)


def print_balance_sheets(sheets: list[BalanceSheet]) -> None:
    """Display balance sheets as a table."""
    rows = [
        ("Cash & Equivalents", "cash_and_equivalents"),
        ("Accounts Receivable", "accounts_receivable"),
        ("Inventory", "inventory"),
        ("Total Current Assets", "total_current_assets"),
        ("PP&E (Net)", "property_plant_equipment"),
        ("Goodwill", "goodwill"),
        ("Total Assets", "total_assets"),
        ("", None),
        ("Accounts Payable", "accounts_payable"),
        ("Short-Term Debt", "short_term_debt"),
        ("Total Current Liabilities", "total_current_liabilities"),
        ("Long-Term Debt", "long_term_debt"),
        ("Total Liabilities", "total_liabilities"),
        ("", None),
        ("Stockholders' Equity", "total_stockholders_equity"),
        ("Retained Earnings", "retained_earnings"),
    ]
    _print_statement_table("Balance Sheet", sheets, rows)


def print_cash_flows(flows: list[CashFlowStatement]) -> None:
    """Display cash flow statements as a table."""
    rows = [
        ("Net Income", "net_income"),
        ("D&A", "depreciation_amortization"),
        ("Stock-Based Comp", "stock_based_compensation"),
        ("Change in WC", "change_in_working_capital"),
        ("Operating CF", "operating_cash_flow"),
        ("", None),
        ("CapEx", "capital_expenditure"),
        ("Acquisitions", "acquisitions"),
        ("Investing CF", "investing_cash_flow"),
        ("", None),
        ("Debt Issuance", "debt_issuance"),
        ("Debt Repayment", "debt_repayment"),
        ("Share Repurchase", "share_repurchase"),
        ("Dividends Paid", "dividends_paid"),
        ("Financing CF", "financing_cash_flow"),
        ("", None),
        ("Free Cash Flow", "free_cash_flow"),
    ]
    _print_statement_table("Cash Flow Statement", flows, rows)


def print_ratios(ratios_list: list[AllRatios]) -> None:
    """Display financial ratios table."""
    if not ratios_list:
        console.print("[dim]No ratio data available.[/dim]")
        return

    # Profitability
    _print_ratio_section(
        "Profitability",
        ratios_list,
        [
            ("Gross Margin", "gross_margin", "gross_margin", True),
            ("Operating Margin", "operating_margin", "operating_margin", True),
            ("Net Margin", "net_margin", "net_margin", True),
            ("EBITDA Margin", "ebitda_margin", "", True),
            ("ROA", "roa", "roa", True),
            ("ROE", "roe", "roe", True),
            ("ROIC", "roic", "roic", True),
            ("ROCE", "roce", "", True),
        ],
        "profitability",
    )

    # Liquidity
    _print_ratio_section(
        "Liquidity",
        ratios_list,
        [
            ("Current Ratio", "current_ratio", "current_ratio", False),
            ("Quick Ratio", "quick_ratio", "quick_ratio", False),
            ("Cash Ratio", "cash_ratio", "", False),
            ("Operating CF Ratio", "operating_cf_ratio", "", False),
        ],
        "liquidity",
    )

    # Solvency
    _print_ratio_section(
        "Solvency",
        ratios_list,
        [
            ("Debt/Equity", "debt_to_equity", "debt_to_equity", False),
            ("Debt/Assets", "debt_to_assets", "", False),
            ("Interest Coverage", "interest_coverage", "interest_coverage", False),
            ("EBITDA/Interest", "ebitda_interest_coverage", "", False),
            ("Net Debt/EBITDA", "net_debt_to_ebitda", "", False),
            ("Debt/FCF", "debt_to_fcf", "", False),
        ],
        "solvency",
    )

    # Efficiency
    _print_ratio_section(
        "Efficiency",
        ratios_list,
        [
            ("Asset Turnover", "asset_turnover", "", False),
            ("Inventory Turnover", "inventory_turnover", "", False),
            ("Receivable Turnover", "receivable_turnover", "", False),
            ("Payable Turnover", "payable_turnover", "", False),
            ("Cash Conv. Cycle (days)", "cash_conversion_cycle", "", False),
        ],
        "efficiency",
    )

    # Valuation (latest only)
    if ratios_list and ratios_list[0].valuation:
        v = ratios_list[0].valuation
        table = Table(title="Valuation", show_lines=True, title_style="bold magenta")
        table.add_column("Metric", style="bold", min_width=20)
        table.add_column("Value", justify="right", min_width=12)

        val_rows = [
            ("P/E Ratio", v.pe_ratio, False),
            ("Forward P/E", v.forward_pe, False),
            ("P/B Ratio", v.pb_ratio, False),
            ("P/S Ratio", v.ps_ratio, False),
            ("P/FCF", v.p_to_fcf, False),
            ("EV/EBITDA", v.ev_to_ebitda, False),
            ("EV/EBIT", v.ev_to_ebit, False),
            ("Earnings Yield", v.earnings_yield, True),
            ("FCF Yield", v.fcf_yield, True),
            ("Dividend Yield", v.dividend_yield, True),
        ]

        for label, val, pct in val_rows:
            if pct:
                table.add_row(label, fmt_number(val, pct=False) if val is None else f"{val * 100:.2f}%")
            else:
                table.add_row(label, fmt_number(val) if val and abs(val) >= 1000 else (f"{val:.2f}" if val is not None else "[dim]—[/dim]"))

        console.print(table)


def _print_ratio_section(
    title: str,
    ratios_list: list[AllRatios],
    rows: list[tuple[str, str, str, bool]],
    category: str,
) -> None:
    """Print a category of ratios as a table across periods."""
    table = Table(title=title, show_lines=True, title_style="bold magenta")
    table.add_column("Metric", style="bold", min_width=22)
    for r in ratios_list:
        table.add_column(r.period_end, justify="right", min_width=12)

    for label, field, color_key, is_pct in rows:
        values = []
        for r in ratios_list:
            cat_obj = getattr(r, category, None)
            val = getattr(cat_obj, field, None) if cat_obj else None
            if color_key:
                values.append(fmt_colored_ratio(color_key, val, pct=is_pct))
            elif is_pct:
                values.append(fmt_number(val, pct=False) if val is None else f"{val * 100:.2f}%")
            else:
                values.append(f"{val:.2f}" if val is not None else "[dim]—[/dim]")
        table.add_row(label, *values)

    console.print(table)
