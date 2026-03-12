"""Color scheme and signal coloring logic."""

from __future__ import annotations

from fundx.cli.formatters.fmt import fmt_number, fmt_ratio  # noqa: F401 — re-export
from fundx.config.defaults import RATIO_THRESHOLDS


def signal_color(metric: str, value: float | None) -> str:
    """Return a Rich color string based on metric threshold.

    Returns 'green' for good, 'yellow' for warning, 'red' for bad, 'white' for unknown.
    """
    if value is None:
        return "dim"

    thresholds = RATIO_THRESHOLDS.get(metric)
    if thresholds is None:
        return "white"

    good = thresholds["good"]
    warning = thresholds["warning"]

    # For metrics where higher is better (most profitability/efficiency ratios)
    if good > warning:
        if value >= good:
            return "green"
        if value >= warning:
            return "yellow"
        return "red"
    # For metrics where lower is better (debt ratios)
    else:
        if value <= good:
            return "green"
        if value <= warning:
            return "yellow"
        return "red"


def fmt_colored_ratio(
    metric: str, value: float | None, decimals: int = 2, pct: bool = False
) -> str:
    """Format a ratio with color coding."""
    if value is None:
        return "[dim]—[/dim]"
    color = signal_color(metric, value)
    if pct:
        text = f"{value * 100:.{decimals}f}%"
    else:
        text = f"{value:.{decimals}f}"
    return f"[{color}]{text}[/{color}]"
