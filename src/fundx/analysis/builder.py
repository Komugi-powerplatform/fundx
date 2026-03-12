"""Builder utilities for constructing analysis results."""

from __future__ import annotations

from fundx.analysis.ratios import AllRatios, calc_all_ratios
from fundx.data.models import BalanceSheet, CashFlowStatement, IncomeStatement, KeyMetrics


def build_ratios_list(
    inc_list: list[IncomeStatement],
    bs_list: list[BalanceSheet],
    cf_list: list[CashFlowStatement],
    metrics: KeyMetrics | None = None,
) -> list[AllRatios]:
    """Build ratio calculations across multiple periods.

    Valuation metrics are only applied to the most recent period.
    """
    ratios_list = []
    for i in range(min(len(inc_list), len(bs_list))):
        cf = cf_list[i] if i < len(cf_list) else None
        m = metrics if i == 0 else None
        ratios_list.append(calc_all_ratios(inc_list[i], bs_list[i], cf, m))
    return ratios_list
