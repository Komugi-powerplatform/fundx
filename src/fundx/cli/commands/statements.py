"""Statements command — display financial statements."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from fundx.cli.formatters.tables import (
    print_balance_sheets,
    print_cash_flows,
    print_income_statements,
)
from fundx.data.providers.yfinance_provider import YFinanceProvider
from fundx.data.resolver import resolve_ticker

console = Console()


def statements(
    query: str = typer.Argument(..., help="Ticker symbol or company name"),
    type: Annotated[str, typer.Option(help="Statement type: income, balance, cashflow, all")] = "all",
    period: Annotated[str, typer.Option(help="Period: annual or quarterly")] = "annual",
    years: Annotated[int, typer.Option(help="Number of periods to display")] = 5,
) -> None:
    """Display financial statements."""
    ticker = resolve_ticker(query)
    if not ticker:
        raise typer.Exit(1)

    provider = YFinanceProvider()

    with console.status(f"[bold]Fetching financial statements for {ticker}...[/bold]"):
        if type in ("income", "all"):
            inc = provider.get_income_statements(ticker, period, years)
            print_income_statements(inc)

        if type in ("balance", "all"):
            bs = provider.get_balance_sheets(ticker, period, years)
            print_balance_sheets(bs)

        if type in ("cashflow", "all"):
            cf = provider.get_cash_flows(ticker, period, years)
            print_cash_flows(cf)
