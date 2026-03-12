"""Default thresholds and benchmarks for analysis."""

# Piotroski F-Score thresholds
PIOTROSKI_STRONG = 7  # 7-9 = strong
PIOTROSKI_WEAK = 3    # 0-3 = weak

# Altman Z-Score zones
ALTMAN_SAFE = 2.99
ALTMAN_GREY = 1.81

# Ratio benchmarks (general, sector-agnostic)
RATIO_THRESHOLDS = {
    "current_ratio": {"good": 1.5, "warning": 1.0},
    "quick_ratio": {"good": 1.0, "warning": 0.5},
    "debt_to_equity": {"good": 1.0, "warning": 2.0},
    "interest_coverage": {"good": 5.0, "warning": 2.0},
    "roe": {"good": 0.15, "warning": 0.08},
    "roa": {"good": 0.08, "warning": 0.03},
    "roic": {"good": 0.12, "warning": 0.06},
    "gross_margin": {"good": 0.40, "warning": 0.20},
    "operating_margin": {"good": 0.15, "warning": 0.05},
    "net_margin": {"good": 0.10, "warning": 0.03},
    "fcf_margin": {"good": 0.10, "warning": 0.02},
}

# Valuation defaults
DCF_PROJECTION_YEARS = 5
DCF_TERMINAL_MULTIPLE = 15.0

# Display
MAX_DISPLAY_YEARS = 10
DEFAULT_DISPLAY_YEARS = 5
CURRENCY_SYMBOLS = {
    "USD": "$",
    "JPY": "¥",
    "EUR": "€",
    "GBP": "£",
}
