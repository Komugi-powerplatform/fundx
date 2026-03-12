"""Search command — find tickers by company name."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from fundx.data.providers.yfinance_provider import YFinanceProvider

console = Console()


def search(query: str = typer.Argument(..., help="Company name or keyword to search")) -> None:
    """Search for stock tickers by company name."""
    provider = YFinanceProvider()
    with console.status(f"[bold]Searching '{query}'...[/bold]"):
        results = provider.search_ticker(query)

    if not results:
        console.print(f"[red]'{query}' に一致する銘柄が見つかりませんでした。[/red]")
        console.print("[dim]ヒント: 日本語は非対応です。英語名で検索してください（例: Toyota, Sony）[/dim]")
        raise typer.Exit(1)

    table = Table(title=f"Search results: '{query}'", show_lines=False)
    table.add_column("Ticker", style="cyan bold")
    table.add_column("Name")
    table.add_column("Exchange", style="dim")

    for r in results[:15]:
        table.add_row(r["ticker"], r["name"], r["exchange"])

    console.print(table)
