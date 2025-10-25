# market_data.py

"""
Market Data Service - Twelve Data Integration

This module fetches real-time and historical market data from Twelve Data API.
"""

from twelvedata import TDClient
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import os


class MarketDataService:
    """Service for fetching market data from Twelve Data."""
    
    # Initialize client (will use API key from environment variable)
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Twelve Data client.
        
        Args:
            api_key: Twelve Data API key. If None, reads from TWELVE_DATA_API_KEY env var
        """
        self.api_key = api_key or os.getenv("TWELVE_DATA_API_KEY")
        if not self.api_key:
            raise ValueError("Twelve Data API key not found. Set TWELVE_DATA_API_KEY environment variable.")
        self.td = TDClient(apikey=self.api_key)
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current stock price.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            
        Returns:
            Current price or None if not found
        """
        try:
            quote = self.td.quote(symbol=ticker).as_json()
            if quote and 'close' in quote:
                return float(quote['close'])
            return None
        except Exception as e:
            print(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def get_stock_info(self, ticker: str) -> dict:
        """
        Get comprehensive stock information.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock info including current price, volume, etc.
        """
        try:
            # Get real-time quote
            quote = self.td.quote(symbol=ticker).as_json()
            
            # Get additional profile data
            try:
                profile = self.td.get_logo(symbol=ticker).as_json()
                company_name = profile.get('name', ticker)
            except:
                company_name = ticker
            
            if not quote:
                return {}
            
            return {
                "ticker": ticker,
                "current_price": float(quote.get('close', 0)),
                "previous_close": float(quote.get('previous_close', 0)),
                "open": float(quote.get('open', 0)),
                "day_high": float(quote.get('high', 0)),
                "day_low": float(quote.get('low', 0)),
                "volume": int(quote.get('volume', 0)),
                "market_cap": None,  # Twelve Data free tier doesn't include market cap
                "company_name": company_name,
            }
        except Exception as e:
            print(f"Error fetching stock info for {ticker}: {e}")
            return {}
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Get historical price data.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period - converts to appropriate interval
                   "1d" -> 1 day, "5d" -> 5 days, "1mo" -> 1 month, etc.
            
        Returns:
            DataFrame with historical OHLCV data
        """
        try:
            # Convert period to outputsize and interval
            period_map = {
                "1d": ("1", "1min"),
                "5d": ("5", "1day"),
                "1mo": ("30", "1day"),
                "3mo": ("90", "1day"),
                "6mo": ("180", "1day"),
                "1y": ("365", "1day"),
                "2y": ("730", "1day"),
                "5y": ("1825", "1day"),
            }
            
            outputsize, interval = period_map.get(period, ("365", "1day"))
            
            # Fetch time series data
            ts = self.td.time_series(
                symbol=ticker,
                interval=interval,
                outputsize=outputsize
            )
            
            df = ts.as_pandas()
            
            if df is not None and not df.empty:
                # Rename columns to match yfinance format
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df.index.name = 'Date'
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_option_chain(self, ticker: str, expiration_date: Optional[str] = None) -> dict:
        """
        Get option chain data for a ticker.
        
        Note: Twelve Data free tier has limited options data.
        This is a placeholder that returns empty data.
        For full options data, consider upgrading or using a different source.
        
        Args:
            ticker: Stock ticker symbol
            expiration_date: Specific expiration date (YYYY-MM-DD), or None for nearest
            
        Returns:
            Dictionary with calls and puts DataFrames
        """
        try:
            # Twelve Data free tier doesn't include full options chain
            # This would require a paid plan or alternative data source
            print(f"Note: Options chain data requires Twelve Data paid plan or alternative source")
            
            return {
                "calls": pd.DataFrame(),
                "puts": pd.DataFrame(),
                "expiration_date": expiration_date or "",
                "available_expirations": []
            }
        except Exception as e:
            print(f"Error fetching option chain for {ticker}: {e}")
            return {"calls": pd.DataFrame(), "puts": pd.DataFrame(), "expirations": []}
    
    def validate_ticker(self, ticker: str) -> bool:
        """
        Check if a ticker symbol is valid.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if valid, False otherwise
        """
        try:
            quote = self.td.quote(symbol=ticker).as_json()
            return quote is not None and 'close' in quote
        except:
            return False


# Create a singleton instance that can be imported
_instance = None

def get_market_data_service(api_key: Optional[str] = None) -> MarketDataService:
    """
    Get or create MarketDataService singleton instance.
    
    Args:
        api_key: Optional API key, otherwise uses environment variable
        
    Returns:
        MarketDataService instance
    """
    global _instance
    if _instance is None:
        _instance = MarketDataService(api_key=api_key)
    return _instance