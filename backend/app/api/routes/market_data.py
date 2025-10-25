"""
Market Data API Routes

FastAPI routes for fetching real market data from Twelve Data.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.option_request import (
    TickerRequest,
    StockInfoResponse,
    HistoricalVolatilityResponse,
    OptionChainResponse,
    OptionData,
    TreasuryRatesResponse
)
from app.services.twelve_data import get_market_data_service
from app.services.volatility import VolatilityService
from app.services.risk_free_rate import RiskFreeRateService
from typing import List

router = APIRouter(prefix="/api/market", tags=["market-data"])


@router.post("/stock-info", response_model=StockInfoResponse)
async def get_stock_info(request: TickerRequest):
    """
    Get current stock information including price, volume, etc.
    
    Args:
        request: Ticker symbol
        
    Returns:
        Stock information
    """
    try:
        market_service = get_market_data_service()
        
        # Validate ticker first
        if not market_service.validate_ticker(request.ticker):
            raise HTTPException(status_code=404, detail=f"Invalid ticker symbol: {request.ticker}")
        
        info = market_service.get_stock_info(request.ticker)
        
        if not info:
            raise HTTPException(status_code=404, detail=f"No data found for ticker: {request.ticker}")
        
        return StockInfoResponse(**info)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock info: {str(e)}")


@router.post("/historical-volatility", response_model=HistoricalVolatilityResponse)
async def get_historical_volatility(
    request: TickerRequest,
    period: str = Query("1y", description="Time period for historical data"),
    window: int = Query(30, ge=2, le=252, description="Rolling window for volatility calculation")
):
    """
    Calculate historical volatility for a stock.
    
    Args:
        request: Ticker symbol
        period: Historical data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
        window: Number of days for volatility calculation
        
    Returns:
        Historical volatility
    """
    try:
        market_service = get_market_data_service()
        
        # Get historical data
        hist_data = market_service.get_historical_data(request.ticker, period)
        
        if hist_data.empty:
            raise HTTPException(status_code=404, detail=f"No historical data found for {request.ticker}")
        
        # Calculate volatility
        volatility = VolatilityService.calculate_historical_volatility(
            hist_data['Close'],
            window=window
        )
        
        return HistoricalVolatilityResponse(
            ticker=request.ticker,
            volatility=volatility,
            window_days=window,
            period=period
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating volatility: {str(e)}")


@router.post("/option-chain", response_model=OptionChainResponse)
async def get_option_chain(
    ticker: str = Query(..., description="Stock ticker symbol"),
    expiration_date: str = Query(None, description="Expiration date (YYYY-MM-DD)")
):
    """
    Get option chain data for a ticker.
    
    Note: Twelve Data free tier has limited options data.
    
    Args:
        ticker: Stock ticker symbol
        expiration_date: Specific expiration date or None for nearest
        
    Returns:
        Option chain with calls and puts
    """
    try:
        market_service = get_market_data_service()
        ticker = ticker.upper().strip()
        
        # Validate ticker
        if not market_service.validate_ticker(ticker):
            raise HTTPException(status_code=404, detail=f"Invalid ticker symbol: {ticker}")
        
        # Get option chain
        chain_data = market_service.get_option_chain(ticker, expiration_date)
        
        if chain_data['calls'].empty and chain_data['puts'].empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No option chain data available. Twelve Data free tier has limited options data."
            )
        
        # Convert DataFrames to list of OptionData
        calls = []
        for _, row in chain_data['calls'].iterrows():
            calls.append(OptionData(
                strike=float(row.get('strike', 0)),
                last_price=float(row.get('lastPrice', 0)),
                bid=float(row.get('bid', 0)) if 'bid' in row else None,
                ask=float(row.get('ask', 0)) if 'ask' in row else None,
                volume=int(row.get('volume', 0)) if 'volume' in row else None,
                open_interest=int(row.get('openInterest', 0)) if 'openInterest' in row else None,
                implied_volatility=float(row.get('impliedVolatility', 0)) if 'impliedVolatility' in row else None
            ))
        
        puts = []
        for _, row in chain_data['puts'].iterrows():
            puts.append(OptionData(
                strike=float(row.get('strike', 0)),
                last_price=float(row.get('lastPrice', 0)),
                bid=float(row.get('bid', 0)) if 'bid' in row else None,
                ask=float(row.get('ask', 0)) if 'ask' in row else None,
                volume=int(row.get('volume', 0)) if 'volume' in row else None,
                open_interest=int(row.get('openInterest', 0)) if 'openInterest' in row else None,
                implied_volatility=float(row.get('impliedVolatility', 0)) if 'impliedVolatility' in row else None
            ))
        
        return OptionChainResponse(
            ticker=ticker,
            expiration_date=chain_data['expiration_date'],
            available_expirations=chain_data['available_expirations'],
            calls=calls,
            puts=puts
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching option chain: {str(e)}")


@router.get("/treasury-rates", response_model=TreasuryRatesResponse)
async def get_treasury_rates():
    """
    Get current Treasury rates for all maturities.
    
    Returns:
        Dictionary of Treasury rates
    """
    try:
        rates = RiskFreeRateService.get_all_rates()
        default_rate = RiskFreeRateService.get_treasury_rate("10Y") or 0.045
        
        return TreasuryRatesResponse(
            rates=rates,
            default_rate=default_rate
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Treasury rates: {str(e)}")


@router.get("/risk-free-rate")
async def get_risk_free_rate(time_to_expiration: float = Query(..., ge=0, description="Time to expiration in years")):
    """
    Get appropriate risk-free rate for given time to expiration.
    
    Args:
        time_to_expiration: Time to expiration in years
        
    Returns:
        Risk-free rate
    """
    try:
        rate = RiskFreeRateService.get_risk_free_rate_for_maturity(time_to_expiration)
        
        return {
            "risk_free_rate": rate,
            "time_to_expiration_years": time_to_expiration
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching risk-free rate: {str(e)}")