# tests for Black-Scholes model

# backend/app/__init__.py
"""
Options Pricing Tool Backend Application
"""

__version__ = "1.0.0"

# backend/app/api/__init__.py
"""
API Package
"""

# backend/app/api/routes/__init__.py
"""
API Routes
"""

# backend/app/models/__init__.py
"""
Pricing Models
"""

from .black_scholes import BlackScholesModel
from .greeks import Greeks

__all__ = ["BlackScholesModel", "Greeks"]

# backend/app/services/__init__.py
"""
External Services
"""

from .market_data import MarketDataService
from .volatility import VolatilityService
from .risk_free_rate import RiskFreeRateService

__all__ = ["MarketDataService", "VolatilityService", "RiskFreeRateService"]

# backend/app/schemas/__init__.py
"""
Pydantic Schemas
"""

# backend/app/utils/__init__.py
"""
Utility Functions
"""

from .validators import (
    validate_option_inputs,
    validate_ticker,
    calculate_time_to_expiration,
    check_arbitrage_bounds
)

__all__ = [
    "validate_option_inputs",
    "validate_ticker", 
    "calculate_time_to_expiration",
    "check_arbitrage_bounds"
]

# backend/tests/__init__.py
"""
Test Suite
"""