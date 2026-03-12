"""Analyze command — full fundamental analysis of a stock."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from fundx.analysis.builder import build_ratios_list
from fundx.cli.formatters.tables import (
    print_balance_sheets,
    print_cash_flows,
    print_income_statements,
    print_profile,
    print_ratios,
)
from fundx.data.providers.yfinance_provider import YFinanceProvider
from fundx.data.resolver import resolve_ticker

console = Console()


def analyze(
    query: str = typer.Argument(..., help="Ticker symbol or company name"),
    period: Annotated[str, typer.Option(help="Period: annual or quarterly")] = "annual",
    years: Annotated[int, typer.Option(help="Number of periods")] = 5,
) -> None:
    """Run full fundamental analysis on a stock."""
    ticker = resolve_ticker(query)
    if not ticker:
        raise typer.Exit(1)

    provider = YFinanceProvider()

    with console.status(f"[bold]Fetching data for {ticker}...[/bold]"):
        data = provider.get_financial_data(ticker, period, years)

    # Company overview
    print_profile(data.profile, data.metrics)
    console.print()

    # Financial statements
    print_income_statements(data.income_statements)
    console.print()
    print_balance_sheets(data.balance_sheets)
    console.print()
    print_cash_flows(data.cash_flows)
    console.print()

    # Ratios
    if data.income_statements and data.balance_sheets:
        ratios_list = build_ratios_list(
            data.income_statements, data.balance_sheets, data.cash_flows, data.metrics
        )
        print_ratios(ratios_list)
