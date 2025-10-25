# api_client.py

"""
API Client for Options Pricing Backend

Handles all HTTP requests to the FastAPI backend.
"""

import httpx
from typing import Optional, Dict, Any


API_BASE_URL = "http://localhost:8000"


async def calculate_option_price(params: Dict[str, Any]) -> Optional[Dict]:
    """Calculate option price and Greeks."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/options/price",
                json=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error calculating option price: {e}")
        return None


async def get_stock_info(ticker: str) -> Optional[Dict]:
    """Get stock information from Twelve Data."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/market/stock-info",
                json={"ticker": ticker},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching stock info: {e}")
        return None


async def get_historical_volatility(ticker: str, period: str = "1y", window: int = 30) -> Optional[Dict]:
    """Get historical volatility."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/market/historical-volatility?period={period}&window={window}",
                json={"ticker": ticker},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching historical volatility: {e}")
        return None


async def get_greeks_surface(params: Dict[str, Any]) -> Optional[Dict]:
    """Get Greeks surface data for visualization."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/options/greeks-surface",
                json=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching Greeks surface: {e}")
        return None


async def calculate_implied_volatility(params: Dict[str, Any]) -> Optional[Dict]:
    """Calculate implied volatility from market price."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/options/implied-volatility",
                json=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error calculating implied volatility: {e}")
        return None


async def get_options_expirations(ticker: str) -> Optional[Dict]:
    """Get available expiration dates for a ticker."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/options-chain/expirations/{ticker}",
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching expirations: {e}")
        return None


async def get_real_options_chain(ticker: str, expiration_date: Optional[str] = None, limit: int = 50) -> Optional[Dict]:
    """Get real options chain from Polygon."""
    try:
        params = {"limit": limit}
        if expiration_date:
            params["expiration_date"] = expiration_date
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/options-chain/chain/{ticker}",
                params=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching options chain: {e}")
        return None


async def get_options_chain_with_quotes(ticker: str, expiration_date: Optional[str] = None, limit: int = 10) -> Optional[Dict]:
    """Get options chain with market quotes."""
    try:
        params = {"limit": limit}
        if expiration_date:
            params["expiration_date"] = expiration_date
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/options-chain/chain-with-quotes/{ticker}",
                params=params,
                timeout=60.0  # Longer timeout as this is slower
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching options chain with quotes: {e}")
        return None


async def get_yahoo_expirations(ticker: str) -> Optional[Dict]:
    """Get available expiration dates from Yahoo Finance."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/options-chain/yahoo/expirations/{ticker}",
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching Yahoo expirations: {e}")
        return None


async def get_yahoo_options_chain(ticker: str, expiration_date: str, limit: int = 50) -> Optional[Dict]:
    """Get options chain from Yahoo Finance with full data."""
    try:
        params = {
            "expiration_date": expiration_date,
            "limit": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/options-chain/yahoo/chain/{ticker}",
                params=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error fetching Yahoo options chain: {e}")
        return None