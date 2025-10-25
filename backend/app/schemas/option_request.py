"""
API Schemas - option_request.py

Pydantic models for request validation and response serialization.
Place this file at: backend/app/schemas/option_request.py
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, List
from datetime import date


# Request Models

class OptionPricingRequest(BaseModel):
    """Request model for option pricing calculation."""
    S: float = Field(..., gt=0, description="Current stock price")
    K: float = Field(..., gt=0, description="Strike price")
    T: float = Field(..., gt=0, description="Time to expiration in years")
    r: float = Field(..., ge=0, le=1, description="Risk-free rate (e.g., 0.05 for 5%)")
    sigma: float = Field(..., gt=0, le=5, description="Volatility (e.g., 0.20 for 20%)")
    option_type: Literal["call", "put"] = Field(..., description="Option type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "S": 100.0,
                "K": 105.0,
                "T": 0.25,
                "r": 0.05,
                "sigma": 0.20,
                "option_type": "call"
            }
        }


class TickerRequest(BaseModel):
    """Request model for ticker-based queries."""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    
    @validator('ticker')
    def uppercase_ticker(cls, v):
        return v.upper().strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL"
            }
        }


class ImpliedVolatilityRequest(BaseModel):
    """Request model for implied volatility calculation."""
    market_price: float = Field(..., gt=0, description="Market price of the option")
    S: float = Field(..., gt=0, description="Current stock price")
    K: float = Field(..., gt=0, description="Strike price")
    T: float = Field(..., gt=0, description="Time to expiration in years")
    r: float = Field(..., ge=0, le=1, description="Risk-free rate")
    option_type: Literal["call", "put"] = Field(..., description="Option type")


class OptionChainRequest(BaseModel):
    """Request model for option chain data."""
    ticker: str = Field(..., min_length=1, max_length=10)
    expiration_date: Optional[str] = Field(None, description="Expiration date (YYYY-MM-DD)")
    
    @validator('ticker')
    def uppercase_ticker(cls, v):
        return v.upper().strip()


# Response Models

class GreeksResponse(BaseModel):
    """Response model for Greeks."""
    delta: float = Field(..., description="Delta: sensitivity to price")
    gamma: float = Field(..., description="Gamma: rate of change of delta")
    theta: float = Field(..., description="Theta: time decay per day")
    vega: float = Field(..., description="Vega: sensitivity to volatility (per 1%)")
    rho: float = Field(..., description="Rho: sensitivity to interest rate (per 1%)")


class OptionPricingResponse(BaseModel):
    """Response model for option pricing."""
    option_price: float
    greeks: GreeksResponse
    inputs: OptionPricingRequest


class StockInfoResponse(BaseModel):
    """Response model for stock information."""
    ticker: str
    current_price: Optional[float]
    previous_close: Optional[float]
    open: Optional[float]
    day_high: Optional[float]
    day_low: Optional[float]
    volume: Optional[int]
    market_cap: Optional[int]
    company_name: Optional[str]


class HistoricalVolatilityResponse(BaseModel):
    """Response model for historical volatility."""
    ticker: str
    volatility: float
    window_days: int
    period: str


class ImpliedVolatilityResponse(BaseModel):
    """Response model for implied volatility."""
    implied_volatility: Optional[float]
    market_price: float
    model_price: Optional[float]
    difference: Optional[float]
    model_config = {"protected_namespaces": ()}  # To avoid Pydantic warning


class OptionData(BaseModel):
    """Individual option data."""
    strike: float
    last_price: float
    bid: Optional[float]
    ask: Optional[float]
    volume: Optional[int]
    open_interest: Optional[int]
    implied_volatility: Optional[float]


class OptionChainResponse(BaseModel):
    """Response model for option chain."""
    ticker: str
    expiration_date: str
    available_expirations: List[str]
    calls: List[OptionData]
    puts: List[OptionData]


class TreasuryRatesResponse(BaseModel):
    """Response model for Treasury rates."""
    rates: dict
    default_rate: float = Field(..., description="Default 10Y rate used for calculations")