"""Ticker resolver — fuzzy company name to ticker symbol."""

from __future__ import annotations

import re

from rich.console import Console
from rich.table import Table

from fundx.data.providers.yfinance_provider import YFinanceProvider

console = Console()


def _looks_like_ticker(query: str) -> bool:
    """Check if query looks like a ticker symbol (e.g. AAPL, 7203.T)."""
    return bool(re.match(r"^[A-Z0-9]{1,5}(\.[A-Z]{1,2})?$", query.upper()))


def resolve_ticker(query: str) -> str | None:
    """Resolve a company name or ticker to a confirmed ticker symbol.

    - If query looks like a ticker, return it directly.
    - Otherwise, search Yahoo Finance and let user pick.

    Returns None if no match found or user cancels.
    """
    if _looks_like_ticker(query):
        return query.upper()

    provider = YFinanceProvider()
    results = provider.search_ticker(query)

    if not results:
        console.print(f"[red]'{query}' に一致する銘柄が見つかりませんでした。[/red]")
        console.print("[dim]ヒント: 日本語は非対応です。英語名で検索してください（例: Toyota, Sony）[/dim]")
        return None

    if len(results) == 1:
        r = results[0]
        console.print(
            f"[green]✓[/green] {r['ticker']}  {r['name']}  ({r['exchange']})"
        )
        return r["ticker"]

    # Multiple results — show table and prompt
    table = Table(title=f"'{query}' の検索結果", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Ticker", style="cyan bold")
    table.add_column("Name")
    table.add_column("Exchange", style="dim")

    display_results = results[:10]
    for i, r in enumerate(display_results, 1):
        table.add_row(str(i), r["ticker"], r["name"], r["exchange"])
    console.print(table)

    try:
        choice = console.input("[bold]選択 (番号 / Enterで1):[/bold] ").strip()
        if not choice:
            idx = 0
        else:
            idx = int(choice) - 1
        if 0 <= idx < len(display_results):
            return display_results[idx]["ticker"]
    except (ValueError, KeyboardInterrupt, EOFError):
        pass

    console.print("[dim]キャンセルしました。[/dim]")
    return None
