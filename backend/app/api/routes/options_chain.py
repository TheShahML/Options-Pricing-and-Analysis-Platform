# options_chain.py

"""
Options Chain API Routes

FastAPI routes for fetching real options chain data from Polygon.io
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from app.services.polygon_service import get_polygon_service
from app.services.yahoo_options_service import get_yahoo_options_service


router = APIRouter(prefix="/api/options-chain", tags=["options-chain"])


# Response Models
class OptionContract(BaseModel):
    """Individual option contract data."""
    ticker: str
    strike_price: float
    expiration_date: str
    contract_type: str
    underlying_ticker: str
    shares_per_contract: Optional[int] = 100
    bid: Optional[float] = None
    ask: Optional[float] = None
    last_price: Optional[float] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None
    implied_volatility: Optional[float] = None
    bs_price: Optional[float] = None
    difference: Optional[float] = None
    percent_difference: Optional[float] = None
    greeks: Optional[dict] = None


class OptionsChainResponse(BaseModel):
    """Options chain response."""
    calls: List[OptionContract]
    puts: List[OptionContract]
    expiration_date: str
    underlying_ticker: str
    total_calls: int
    total_puts: int
    risk_free_rate: Optional[float] = None
    treasury_maturity: Optional[str] = None


class ExpirationsResponse(BaseModel):
    """Available expiration dates response."""
    ticker: str
    expirations: List[str]
    count: int


@router.get("/expirations/{ticker}", response_model=ExpirationsResponse)
async def get_expirations(
    ticker: str,
    limit: int = Query(20, ge=1, le=50, description="Number of expiration dates to return")
):
    """
    Get available expiration dates for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        limit: Maximum number of dates to return
        
    Returns:
        List of expiration dates
    """
    try:
        polygon = get_polygon_service()
        expirations = polygon.get_available_expirations(ticker.upper(), limit=limit)
        
        if not expirations:
            raise HTTPException(
                status_code=404, 
                detail=f"No expiration dates found for {ticker}"
            )
        
        return ExpirationsResponse(
            ticker=ticker.upper(),
            expirations=expirations,
            count=len(expirations)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching expirations: {str(e)}")


@router.get("/chain/{ticker}", response_model=OptionsChainResponse)
async def get_options_chain(
    ticker: str,
    expiration_date: Optional[str] = Query(None, description="Expiration date (YYYY-MM-DD)"),
    strike_price: Optional[float] = Query(None, description="Filter by strike price"),
    limit: int = Query(50, ge=1, le=100, description="Max contracts per type")
):
    """
    Get options chain for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        expiration_date: Filter by expiration date
        strike_price: Filter by strike price
        limit: Maximum contracts to return per type
        
    Returns:
        Options chain with calls and puts
    """
    try:
        polygon = get_polygon_service()
        ticker = ticker.upper()
        
        # Get calls
        calls = polygon.get_options_chain(
            ticker=ticker,
            expiration_date=expiration_date,
            strike_price=strike_price,
            contract_type="call"
        )[:limit]
        
        # Get puts
        puts = polygon.get_options_chain(
            ticker=ticker,
            expiration_date=expiration_date,
            strike_price=strike_price,
            contract_type="put"
        )[:limit]
        
        if not calls and not puts:
            raise HTTPException(
                status_code=404,
                detail=f"No options found for {ticker}"
            )
        
        # Convert to Pydantic models
        calls_contracts = [OptionContract(**call) for call in calls]
        puts_contracts = [OptionContract(**put) for put in puts]
        
        return OptionsChainResponse(
            calls=calls_contracts,
            puts=puts_contracts,
            expiration_date=expiration_date or "multiple",
            underlying_ticker=ticker,
            total_calls=len(calls_contracts),
            total_puts=len(puts_contracts)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching options chain: {str(e)}")


@router.get("/chain-with-quotes/{ticker}")
async def get_options_chain_with_quotes(
    ticker: str,
    expiration_date: Optional[str] = Query(None, description="Expiration date (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=20, description="Max contracts per type (limited for rate limits)")
):
    """
    Get options chain with current market quotes.
    Note: Limited to 10 contracts per type to avoid rate limits on free tier.
    
    Args:
        ticker: Stock ticker symbol
        expiration_date: Filter by expiration date
        limit: Maximum contracts to return per type (max 20)
        
    Returns:
        Options chain with market quotes
    """
    try:
        polygon = get_polygon_service()
        ticker = ticker.upper()
        
        chain_data = polygon.get_options_chain_with_quotes(
            ticker=ticker,
            expiration_date=expiration_date,
            limit=limit
        )
        
        if not chain_data['calls'] and not chain_data['puts']:
            raise HTTPException(
                status_code=404,
                detail=f"No options with quotes found for {ticker}"
            )
        
        return {
            "calls": chain_data['calls'],
            "puts": chain_data['puts'],
            "expiration_date": chain_data['expiration_date'],
            "underlying_ticker": chain_data['underlying_ticker'],
            "total_calls": len(chain_data['calls']),
            "total_puts": len(chain_data['puts']),
            "note": "Limited to 10 contracts per type to respect API rate limits"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chain with quotes: {str(e)}")


@router.get("/yahoo/expirations/{ticker}", response_model=ExpirationsResponse)
async def get_yahoo_expirations(
    ticker: str,
    limit: int = Query(20, ge=1, le=50, description="Number of expiration dates to return")
):
    """
    Get available expiration dates from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
        limit: Maximum number of dates to return
        
    Returns:
        List of expiration dates
    """
    try:
        yahoo = get_yahoo_options_service()
        expirations = yahoo.get_available_expirations(ticker.upper(), limit=limit)
        
        if not expirations:
            raise HTTPException(
                status_code=404, 
                detail=f"No expiration dates found for {ticker}"
            )
        
        return ExpirationsResponse(
            ticker=ticker.upper(),
            expirations=expirations,
            count=len(expirations)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching expirations: {str(e)}")


@router.get("/yahoo/chain/{ticker}", response_model=OptionsChainResponse)
async def get_yahoo_chain(
    ticker: str,
    expiration_date: str = Query(..., description="Expiration date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=100, description="Max contracts per type")
):
    """Get options chain from Yahoo Finance with full market data."""
    try:
        yahoo = get_yahoo_options_service()
        ticker = ticker.upper()
        
        chain_data = yahoo.get_options_chain_formatted(ticker, expiration_date, limit=limit)
        
        if not chain_data['calls'] and not chain_data['puts']:
            raise HTTPException(
                status_code=404,
                detail=f"No options found for {ticker} on {expiration_date}"
            )
        
        # Convert to Pydantic models
        calls_contracts = [OptionContract(**call) for call in chain_data['calls']]
        puts_contracts = [OptionContract(**put) for put in chain_data['puts']]
        
        return OptionsChainResponse(
            calls=calls_contracts,
            puts=puts_contracts,
            expiration_date=expiration_date,
            underlying_ticker=ticker,
            total_calls=len(calls_contracts),
            total_puts=len(puts_contracts),
            risk_free_rate=chain_data.get('risk_free_rate'),
            treasury_maturity=chain_data.get('treasury_maturity')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Yahoo options chain: {str(e)}")