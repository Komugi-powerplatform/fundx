"""Shared math utilities for analysis."""

from __future__ import annotations


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    """Safe division returning None if inputs are None or denominator is zero."""
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def safe_pct(value: float | None) -> float | None:
    """Convert ratio to percentage (e.g. 0.15 -> 15.0). Returns None if input is None."""
    if value is None:
        return None
    return value * 100


def cagr(begin: float | None, end: float | None, years: int) -> float | None:
    """Compound Annual Growth Rate."""
    if begin is None or end is None or years <= 0 or begin <= 0 or end <= 0:
        return None
    return (end / begin) ** (1 / years) - 1


def yoy_growth(current: float | None, previous: float | None) -> float | None:
    """Year-over-year growth rate."""
    if current is None or previous is None or previous == 0:
        return None
    return (current - previous) / abs(previous)
