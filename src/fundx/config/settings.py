"""Application settings loaded from environment and config file."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global configuration for fundx."""

    model_config = {"env_prefix": "FUNDX_"}

    # API keys (optional — yfinance works without any)
    fmp_api_key: str = ""
    alphavantage_api_key: str = ""

    # Cache
    cache_dir: str = "~/.fundx/cache"
    cache_ttl_hours: int = 24

    # Default analysis parameters
    default_wacc: float = 0.10
    default_terminal_growth: float = 0.025
    default_risk_free_rate: float = 0.04
    default_years: int = 5


settings = Settings()
