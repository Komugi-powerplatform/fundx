"""Pure formatting helpers (no color, no Rich markup except dim placeholder)."""

from __future__ import annotations


def fmt_number(value: float | None, decimals: int = 2, pct: bool = False) -> str:
    """Format a number for display."""
    if value is None:
        return "[dim]—[/dim]"
    if pct:
        return f"{value * 100:.{decimals}f}%"
    if abs(value) >= 1e12:
        return f"{value / 1e12:.{decimals}f}T"
    if abs(value) >= 1e9:
        return f"{value / 1e9:.{decimals}f}B"
    if abs(value) >= 1e6:
        return f"{value / 1e6:.{decimals}f}M"
    if abs(value) >= 1e3:
        return f"{value / 1e3:.{decimals}f}K"
    return f"{value:.{decimals}f}"


def fmt_ratio(value: float | None, decimals: int = 2) -> str:
    """Format a ratio value."""
    if value is None:
        return "[dim]—[/dim]"
    return f"{value:.{decimals}f}"
