"""Ratios command — display financial ratios."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from fundx.analysis.builder import build_ratios_list
from fundx.cli.formatters.tables import print_ratios
from fundx.data.providers.yfinance_provider import YFinanceProvider
from fundx.data.resolver import resolve_ticker

console = Console()


def ratios(
    query: str = typer.Argument(..., help="Ticker symbol or company name"),
    period: Annotated[str, typer.Option(help="Period: annual or quarterly")] = "annual",
    years: Annotated[int, typer.Option(help="Number of periods")] = 5,
) -> None:
    """Display financial ratios across multiple periods."""
    ticker = resolve_ticker(query)
    if not ticker:
        raise typer.Exit(1)

    provider = YFinanceProvider()

    with console.status(f"[bold]Analyzing {ticker}...[/bold]"):
        inc_list = provider.get_income_statements(ticker, period, years)
        bs_list = provider.get_balance_sheets(ticker, period, years)
        cf_list = provider.get_cash_flows(ticker, period, years)
        metrics = provider.get_key_metrics(ticker)

    if not inc_list or not bs_list:
        console.print("[red]Financial data not available.[/red]")
        raise typer.Exit(1)

    ratios_list = build_ratios_list(inc_list, bs_list, cf_list, metrics)

    print_ratios(ratios_list)
